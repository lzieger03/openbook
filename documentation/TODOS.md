# OpenBook – Bekannte Einschränkungen & offene Punkte (TODOs)

Diese Datei sammelt **bewusst noch offene Punkte, Demo-Funktionen und bekannte
Einschränkungen**. Sie ist die zentrale Anlaufstelle für „Warum verhält sich X gerade
so?" und „Was muss hier noch gemacht werden?". Bitte hier ergänzen, wenn etwas bewusst
unfertig gemerged wird.

Legende der Priorität: 🔴 hoch · 🟡 mittel · 🟢 niedrig / nice-to-have.

---

## Teacher-Bereich (Frontend + Backend)

### 🟡 Speichern von Inhalten blockiert die UI (synchrone RAG-Verarbeitung)
- **Beobachtung:** Auf der Teacher-Seite **lädt es lange**, wenn Inhalt
  **hinzugefügt/gespeichert/importiert** wird. Das ist **kein Bug**, sondern die
  RAG-Synchronisation.
- **Ursache:** `TextbookPageViewSet.perform_create/perform_update` ruft
  `TextbookDocumentSyncService().sync_textbook(...)` **synchron im Request** auf
  (`src/openbook/content/viewsets/textbook_page.py`). Der Service rendert das Textbook zu
  Markdown, zerlegt es in Chunks, berechnet **Embeddings** und schreibt den Vektorindex
  neu (`_rebuild_index`). Die UI wartet, bis das fertig ist.
- **TODO:**
  - RAG-Sync in einen **asynchronen Hintergrund-Job** auslagern (z. B. Channels-Worker /
    Task-Queue), damit „Save page" sofort zurückkehrt.
  - `AssistantDocument.index_status` (`pending/indexing/indexed/…`) im Teacher-UI
    anzeigen, statt die Seite zu blockieren.
  - Optional: Debounce/Batching, wenn mehrere Seiten kurz nacheinander gespeichert werden.
- **Bis dahin:** In der UI ist ein Spinner sichtbar – nicht doppelt klicken, Seite nicht
  neu laden. Dokumentiert in `frontend-teacher.md` §6/§9.

---

## Gamification – Mini-Spiele (Memory / Flashcards / Hangman)

Die Spiele im Dashboard-Hub (`/games/:id`) sind **Demo / Machbarkeitsstudie** und
**noch nicht vollständig implementiert**.

### 🔴 Spielen vergibt keine Punkte (keine Gamification-Anbindung)
- **Beobachtung:** Memory, Flashcards und Hangman geben **keine Punkte**, kein Level,
  keinen Streak, keine Skills.
- **Ursache:** Die Spielseiten
  (`src/frontend/dashboard/src/components/pages/{Memory,Flashcards,Hangman}GamePage.svelte`)
  rufen **keinen** `award_*`-Service auf und erzeugen **keinen** `RewardEventLog`. Die
  Aktivitätsart `GAME_PLAYED` existiert in
  `src/openbook/gamification/constants.py`, ist aber **nirgends im Produktivpfad
  verdrahtet** (nur in `tests/test_streak.py` referenziert).
- **TODO:**
  - Spielabschluss/-fortschritt an die Gamification anbinden, z. B. über
    `record_learning_activity(account_id, GAME_PLAYED)` (Streak) und/oder
    `award_course_points(...)` (Kurspunkte) – mit **Anti-Farming** analog zum Quiz
    (verbesserungsbasiert / Tageslimit), damit Spiele nicht beliebig „gefarmt" werden.
  - Ggf. Skill-Fortschritt über die Seiten-Skills der genutzten Begriffe.

### 🟡 Begriffe stammen nur aus dem Textbook, nicht aus der KI
- **Beobachtung:** Memory & Hangman verwenden **nur Wörter/Begriffe, die bereits im
  Textbook stehen** – es gibt **keine KI-generierten** Begriffe oder
  Antwortmöglichkeiten/Distraktoren.
- **Ursache:** `src/frontend/dashboard/src/data/course-terms.ts` extrahiert Begriffe aus
  dem **gerenderten HTML** der Kursseiten (Überschriften, fett/kursiv, `code`, kurze
  Listenpunkte); Flashcards bilden Überschrift→Abschnitt-Paare.
- **TODO:**
  - KI-gestützte Begriffs-/Distraktor-Generierung (analog zum bestehenden Quiz-Flow über
    den Assistant-Orchestrator), damit die Spiele über das wörtliche Textbook-Vokabular
    hinausgehen.
  - Qualitäts-/Längenfilter und Deduplizierung der extrahierten Begriffe verbessern.

### 🟢 Hub-Hinweis veraltet
- Der Komponentenkommentar in `GamesPage.svelte` sagt sinngemäß „Memory is playable
  today, more can be added later", obwohl inzwischen **alle drei** Spiele geroutet sind.
  Kommentar aktualisieren.

---

## Sonstige bekannte Punkte

### 🟢 Flaky/sortierungs-abhängiger Gamification-Test
- `Reward_ViewSet_Tests.test_list_sort` vergleicht serialisierte **Decimal-Strings
  lexikographisch** und kann dadurch fehlschlagen, ohne dass ein echtes Problem vorliegt
  (siehe `gamification-api-route-fix.md`). Test/Helper robust machen.

### 🟢 Seed-Daten: Punkte/Level leicht inkonsistent
- `load_gamification_dummy_data` legt `AccountProgress` mit `point_total=100`, aber
  `level=1` an, obwohl `LevelThreshold` bei 100 Punkten bereits Level 2 ergäbe. Für reine
  Testdaten unkritisch; bei Bedarf das Level aus `LevelThreshold.level_for_points()`
  ableiten. (Das umfassende Seed-Command ist `openbook/core/management/commands/seed_demo.py`.)

---

## Pflegehinweis

Wenn ein Punkt erledigt ist: hier entfernen **und** den entsprechenden Hinweis in der
jeweiligen Detail-Doku (`frontend-teacher.md`, `frontend-dashboard.md`, `gamification.md`)
mit anpassen, damit Doku und Code nicht auseinanderlaufen.
