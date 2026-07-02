# Gamification – Vollständige Dokumentation

Diese Doku beschreibt das komplette Gamification-System von OpenBook: Datenmodell,
Services, Signals, REST-API und die Anbindung von Lernaktivitäten (Quiz, Seiten,
Kursabschluss). Code liegt in `src/openbook/gamification/` (plus die Lern-Brücke in
`src/openbook/learning/` und `src/openbook/assistant/`).

---

## 1. Überblick & Mentales Modell

Lernende sammeln **Punkte**, steigen in **Levels** auf, halten einen **Daily Streak**
und verbessern **Skills**. Punkte werden sowohl **global** (über den ganzen Account)
als auch **pro Kurs** geführt.

Es gibt **einen einzigen Schreibpfad** für Punkte:

```
award_points-Service (z. B. award_course_points)
        │  schreibt einen RewardEventLog-Eintrag (point delta)
        ▼
post_save-Signal auf RewardEventLog
        │
        ├─► AccountProgress.point_total  +=  delta
        ├─► AccountProgress.level         =  LevelThreshold.level_for_points(total)
        └─► Streak wird fortgeschrieben (bei echten Punkt-Events)
```

Dadurch ist garantiert: Wer Punkte vergibt, aktualisiert **automatisch** das globale
Punktekonto, das Level und den Streak – ohne dass der Aufrufer daran denken muss.

---

## 2. Datenmodell (`gamification/models/`)

| Modell | Zweck | Wichtige Felder |
|---|---|---|
| `AccountProgress` | Globaler Punktestand & Level pro Account | `account` (1:1), `point_total`, `level`, `updated_at` |
| `CourseProgress` | Punkte/Level/Fortschritt **pro Kurs** | `account`, `course`, `course_points`, `course_level`, `course_progress` (0–100 %) |
| `LevelThreshold` | Punkte-Schwellen je Level (global **und** pro Kurs genutzt) | `level` (unique), `min_points` |
| `AccountStreak` | Tages-Streak | `current_streak`, `longest_streak`, `last_active_date`, `last_active_at`, `streak_freezes` |
| `AccountActivityDay` | Eine Zeile pro Account & Kalendertag mit Aktivität | `account`, `activity_date`, `activity_count`, `first/last_activity_at` |
| `Skill` | Globaler Skill-Katalog | `name` (unique), `description`, `icon_path` |
| `SkillProgress` | Skill-Fortschritt pro Account | `account`, `skill`, `level` (Start 1), `progress` (0–100 %) |
| `Reward` | Vordefinierte Belohnung (Typ + Wert) | `reward_type`, `value`, `description` |
| `RewardEventLog` | **Append-only Audit-Log** aller Punkt-Events | `account`, `reward` (opt.), `event_type`, `points_delta`, `context` (JSON), `created_at` |

Hinweise:
- `CourseProgress.course_progress` und der globale Level-Balken werden **beide** aus
  `LevelThreshold` berechnet (`progress_to_next_level`).
- `RewardEventLog.context` (JSON) trägt Kontext wie `page_id`, `score`, `source` und
  ist die Basis für das Anti-Farming der Quizpunkte (siehe §5).

---

## 3. Level-System (`LevelThreshold`)

- `LevelThreshold.level_for_points(points)` → höchstes Level, dessen `min_points`
  erreicht ist (Fallback Level 1).
- `LevelThreshold.progress_to_next_level(points)` → 0–100 % vom aktuellen
  Level-Schwellenwert bis zum nächsten; springt bei jedem Level-Up auf 0 zurück und
  ist 100 %, sobald das höchste konfigurierte Level erreicht ist.
- Schwellen werden über Fixtures/Seed-Daten oder Admin gepflegt. Ohne Schwellen
  bleibt alles auf Level 1.

---

## 4. Streak-System (`services/streak.py`)

- `record_learning_activity(account_id, activity_type)` registriert eine Aktivität
  (siehe `LearningActivityType`) und schreibt ggf. `AccountActivityDay` + Streak fort.
- `update_streak_for_points(account_id, occurred_at)` wird automatisch vom
  RewardEventLog-Signal aufgerufen, wenn ein **echtes** Punkt-Event entsteht.
- Tageslogik nutzt die Zeitzone `Europe/Berlin` (`BERLIN_TZ`).
- Streak-Events landen ebenfalls im `RewardEventLog` (mit `points_delta = 0`, damit das
  Signal nicht rekursiv neue Streaks auslöst – siehe `StreakEventType`).
- `get_streak_state(account_id)` liefert den aktuellen Streak-Zustand.

---

## 5. Punkte- & Skill-Vergabe (Services)

### `services/course.py`
- `award_course_points(account_id, course_id, points, *, reward=None, event_type=None, context=None)`
  – zentraler Einstieg. Erhöht `CourseProgress` (Punkte, Level, Fortschritt), schreibt
  einen `RewardEventLog` (→ globales Konto + Streak via Signal). `@transaction.atomic`.
- `get_course_progress_state(account_id, course_id)` → aktueller Kurs-Zustand als dict.

### `services/skill.py`
- `award_skill_progress(account_id, skill_id, amount)` – erhöht `SkillProgress.progress`;
  bei Überlauf >100 % steigt das Skill-Level (Überschuss wird übertragen). **Legt eine
  fehlende `SkillProgress` automatisch auf Level 1 an** (`get_or_create`).
- `get_skill_progress_state(account_id, skill_id)` → Level + Progress (Default Level 1, 0 %).

### `services/learning_rewards.py` – die Brücke Lernen → Punkte
- `award_quiz_rewards(account_id, course_id, page_id, score, skill_ids=None)`:
  - Kurspunkte = `round(score * QUIZ_MAX_COURSE_POINTS)` (Standard `QUIZ_MAX_COURSE_POINTS = 50`).
  - **Anti-Farming:** nur die **Verbesserung** gegenüber dem bisher besten Score wird
    gutgeschrieben (Summe der bisherigen `QUIZ_POINTS_AWARDED`-Events pro `page_id`).
  - Pro vergebenem Quizpunkt werden `QUIZ_SKILL_PROGRESS_PER_POINT` (Standard 0.5) %
    Skill-Fortschritt auf alle übergebenen `skill_ids` verteilt.
- `award_chat_question_reward(account_id, course_id)`: kleine Pauschale fürs Stellen
  einer Frage im Kurs-Chat (`CHAT_QUESTION_POINTS = 5`), gedeckelt auf
  `CHAT_QUESTION_DAILY_LIMIT = 10` belohnte Fragen pro Tag & Kurs.

### `services/backfill.py`
- Einmaliges Nachziehen/Reparieren von Streak-/Progress-Daten (Management-Command
  `backfill_streaks`).

---

## 6. Signals (`gamification/signals.py`)

- `post_save(User)` → legt `AccountProgress` (Level 1, 0 Punkte) für neue User an.
- `post_save(RewardEventLog)` → **der zentrale Pfad**: addiert `points_delta` aufs
  Konto, berechnet das Level neu (`LevelThreshold`), stößt den Streak an (nur bei
  `points_delta != 0` und Nicht-Streak-Events).
- `post_save / post_delete(RoleAssignment)` → legt eine leere `CourseProgress`-Zeile an,
  wenn ein Student in einen Kurs eingeschrieben wird (damit der Kurs sofort im Dashboard
  erscheint), und entfernt sie bei Ausschreibung **nur**, wenn noch keine Punkte da sind.

Zusätzlich in der Lern-App `learning/signals.py`:
- `post_save(LearningState)` → `record_learning_activity(..., CONTENT_VIEWED)` hält den
  Daily-Streak am Leben, wenn der User Inhalte aufruft.

---

## 7. Anbindung der Lernaktivitäten

### Quiz (über WebSocket / Orchestrator)
1. Frontend schließt ein Quiz ab → WS-Nachricht `learning_quiz_result`
   (`page_id`, `score`, `attempts`).
2. `ai/consumers/chat.py` → `AssistantOrchestrator.record_quiz_result(...)`:
   - speichert `QuizResult`,
   - ruft `award_quiz_rewards(...)` (Kurspunkte + Skills der Textbook-Seiten),
   - gibt die vergebenen Punkte/Skills zurück (für sofortiges UI-Feedback).
- **Wichtig:** Der ChatConsumer hat `camelize = False`. Sonst würde chanx ausgehende
  Felder camelCasen (`page_id` → `pageId`) und das snake_case-Frontend würde sie
  übersehen → keine Punkte. (Siehe Doku-Hinweis ganz unten.)

### Seiten & Kursabschluss (REST, App `learning`)
Drei Endpoints unter `/api/learning/states/` (User aus dem Login, CSRF nötig):

| Endpoint | Wirkung | Gamification |
|---|---|---|
| `POST record-page-opened/` `{course, page}` | setzt `last_page` | Streak (über LearningState-Signal) |
| `POST mark-page-completed/` `{course, page}` | ergänzt `completed_pages` | Streak |
| `POST complete-course/` `{course}` | setzt `is_completed=True` | **+200 Kurspunkte** (`award_course_points`, nur beim ersten Mal) |

Alle drei liefern den aktualisierten `LearningState` (`is_completed`, `completed_pages`,
`last_page`). Das Dashboard ruft sie aus `ContentPage.svelte` auf (siehe Dashboard-Doku).

---

## 7b. Mini-Spiele (Memory / Flashcards / Hangman) – **noch nicht angebunden**

Im Dashboard gibt es einen **Spiele-Hub** pro Kurs (`/games/:id`) mit drei Mini-Spielen.
Sie sind aktuell eine **Demo / Machbarkeitsstudie** und **nicht in die Gamification
integriert**:

- **Keine Punkte fürs Spielen.** Die Spielseiten rufen **keinen** `award_*`-Service auf
  und erzeugen **keinen** `RewardEventLog`. Spielen verändert weder Punkte noch Level,
  Streak oder Skills.
- Die Aktivitätsart **`GAME_PLAYED`** existiert in `constants.py`
  (`LearningActivityType`), wird aber **nirgends im Produktivpfad ausgelöst** (nur in
  einem Streak-Test referenziert). Sie ist der vorgesehene Aufhänger für eine spätere
  Anbindung.
- **Inhaltsquelle = nur das Textbook.** Memory und Hangman verwenden ausschließlich
  Begriffe, die **bereits im Seiteninhalt** stehen (Frontend `data/course-terms.ts`,
  extrahiert aus dem gerenderten HTML). Es gibt **noch keine KI-generierten** Begriffe
  oder Antwortmöglichkeiten.

Geplante nächste Schritte (z. B. Punkte/Streak via `record_learning_activity` +
`award_course_points`, KI-gestützte Begriffe) stehen in `TODOS.md`.

---

## 8. REST-API (`/api/gamification/...`)

Routen in `gamification/routes.py` (registriert mit Prefix `gamification`):

| Ressource | Pfad | Methoden / Custom-Action |
|---|---|---|
| Account Progress | `/api/gamification/account_progress/` | list/retrieve (read-only) |
| – eigener Stand | `/api/gamification/account_progress/me/` | `GET` → `point_total, level, current_level_min_points, next_level_min_points` |
| – Bestenliste | `/api/gamification/account_progress/leaderboard/` | `GET` → Top 10: `rank, username, full_name, level, point_total, is_current_user` |
| Course Progress | `/api/gamification/course_progress/` | list/retrieve, filterbar nach `account`, `course` |
| – Punkte vergeben | `/api/gamification/course_progress/award/` | `POST` `{account?, course, points, skill?, skill_points?}` (Staff/eigener Account) |
| Skills | `/api/gamification/skills/` | **CRUD** – Lesen öffentlich, Anlegen/Ändern/Löschen mit Permission |
| Skill Progress | `/api/gamification/skill_progress/` | list/retrieve (auf eigenen Account gefiltert) |
| Rewards | `/api/gamification/rewards/` | CRUD |
| Reward Event Log | `/api/gamification/reward_event_log/` | list/retrieve |
| – Event auslösen | `/api/gamification/reward_event_log/trigger/` | `POST` (Test/Debug) |
| Activity | `/api/gamification/activity/` | Aktivitätstage |
| Streak | `/api/gamification/streak/` | aktueller Streak |

Flex-Fields werden unterstützt (`_expand`, `_fields`, `_omit`, `_sort`, `_page_size`).

---

## 9. Konstanten (`gamification/constants.py`)

- `LearningActivityType`: `CHAT_MESSAGE_SENT, QUIZ_ANSWERED, QUIZ_COMPLETED, CONTENT_VIEWED, MODULE_COMPLETED, GAME_PLAYED` (Login zählt **nicht**). ⚠️ `GAME_PLAYED` ist **definiert, aber noch ungenutzt** – die Mini-Spiele lösen es nicht aus (siehe §7b).
- `CourseEventType`: `COURSE_POINTS_AWARDED, QUIZ_POINTS_AWARDED, CHAT_POINTS_AWARDED`.
- `StreakEventType`: `STREAK_STARTED, STREAK_INCREMENTED, STREAK_RESET, STREAK_ALREADY_COUNTED_TODAY, LEARNING_ACTIVITY_RECORDED`.

---

## 10. Tests

`gamification/tests/` deckt u. a. ab: `test_skill_award`, `test_skill_progress`,
`test_course_progress`, `test_account_progress`, `test_level_threshold`, `test_streak`,
`test_reward`, `test_reward_event_log`, `test_signals`, `test_learning_rewards`,
`test_backfill`. Lernseite: `learning/tests/`. Quiz-Reward end-to-end:
`ai/tests/test_chat_consumer.py` + `assistant/tests/`.

Ausführen (schnellere Py-3.13-venv):
```
cd src && ../.venv313/bin/python manage.py test openbook.gamification openbook.learning
```

---

## 11. Stolperfallen (wichtig fürs Team)

- **Nach jedem Merge `python manage.py migrate` ausführen.** Häufigste Fehlerquelle sind
  „no such column"-Fehler durch nicht angewendete Migrationen.
- **WebSocket spricht snake_case.** `ChatConsumer.camelize = False` muss bleiben, sonst
  brechen Quiz-Punkte/Skills (Felder wie `page_id`/`points_awarded` würden camelCase).
- **Quizpunkte sind verbesserungsbasiert** (Anti-Farming): Ein erneuter Versuch mit
  gleichem/niedrigerem Score gibt 0 Punkte – das ist beabsichtigt.
