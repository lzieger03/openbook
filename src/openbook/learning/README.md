# openbook_learning

Verfolgt den Lernfortschritt der Nutzer für den KI-Tutor (ELISA).
Der Orchestrator liest diese Daten beim Login und gibt sie als Kontext an das LLM weiter.

---

## Modelle

### LearningState
Eine Zeile pro User+Kurs. Wird aktualisiert sobald der Nutzer eine Seite öffnet oder ein Kapitel abschließt.

| Feld              | Typ                          | Beschreibung                                          |
|-------------------|------------------------------|-------------------------------------------------------|
| `id`              | UUID                         | Primärschlüssel                                       |
| `user`            | FK → User                    | Der Lernende (automatisch aus Login-Token)            |
| `course`          | FK → Course                  | Der Kurs in dem der Nutzer eingeschrieben ist         |
| `last_page`       | FK → TextbookPage (nullable) | Zuletzt besuchte Seite                                |
| `completed_pages` | M2M → TextbookPage           | Alle abgeschlossenen Kapitel                          |
| `last_accessed`   | DateTimeField                | Wird bei jedem Schreibzugriff automatisch aktualisiert |

Constraint: eindeutig pro `user + course`.

### QuizResult
Eine Zeile pro User+Seite. Wird nach jedem Quiz-Versuch aktualisiert (Score wird überschrieben, Versuche hochgezählt).

| Feld          | Typ               | Beschreibung                                           |
|---------------|-------------------|--------------------------------------------------------|
| `id`          | UUID              | Primärschlüssel                                        |
| `user`        | FK → User         | Der Lernende (automatisch aus Login-Token)             |
| `page`        | FK → TextbookPage | Das Kapitel zu dem das Quiz gehört                     |
| `score`       | Float             | Normierter Score 0.0–1.0                               |
| `attempts`    | Integer           | Wie oft das Quiz bereits gemacht wurde                 |
| `answered_at` | DateTimeField     | Wird bei jedem Schreibzugriff automatisch aktualisiert |

Constraint: eindeutig pro `user + page`.

---

## API Endpoints

Basispfad: `/api/learning/`

| Methode | Endpoint                           | Beschreibung                                      |
|---------|------------------------------------|---------------------------------------------------|
| GET     | `/api/learning/states/`            | Lernstände des aktuellen Nutzers abrufen          |
| POST    | `/api/learning/states/`            | Neuen Lernstand anlegen                           |
| PATCH   | `/api/learning/states/{id}/`       | Letzte Seite oder abgeschlossene Kapitel updaten  |
| GET     | `/api/learning/quiz-results/`      | Quiz-Ergebnisse des aktuellen Nutzers abrufen     |
| POST    | `/api/learning/quiz-results/`      | Quiz-Ergebnis anlegen                             |
| PATCH   | `/api/learning/quiz-results/{id}/` | Score aktualisieren + Versuche hochzählen         |

Alle Endpoints erfordern Authentifizierung. Jeder Nutzer sieht nur seine eigenen Daten.

Vollständige Dokumentation: `http://localhost:8000/api/schema/redoc/`

---

## Für den Orchestrator

**Beim Login — aktuellen Stand laden:**
```
GET /api/learning/states/?course=<Course UUID>
```
Antwort enthält `last_page`, `completed_pages` und `last_accessed` — damit baut der Orchestrator den LLM-Kontext.

**Wenn der Nutzer eine Seite öffnet:**
```
PATCH /api/learning/states/{id}/
{ "last_page": "<TextbookPage UUID>" }
```
Falls noch kein Lernstand für diesen Kurs existiert, zuerst anlegen:
```
POST /api/learning/states/
{ "course": "<Course UUID>", "last_page": "<TextbookPage UUID>" }
```

**Wenn der Nutzer ein Kapitel abschließt:**
```
PATCH /api/learning/states/{id}/
{ "completed_pages": ["<TextbookPage UUID>", ...] }
```

**Beispiel Kontext-String für das LLM:**
```python
from openbook.learning.models import LearningState, QuizResult

state = LearningState.objects.filter(user=user, course=course).prefetch_related("completed_pages").select_related("last_page").first()
quizzes = QuizResult.objects.filter(user=user).select_related("page")

kontext = ""
if state:
    kontext += f"Der Nutzer ist im Kurs '{state.course.name}'. "
    kontext += f"Abgeschlossene Kapitel: {state.completed_pages.count()}. "
    if state.last_page:
        kontext += f"Zuletzt gelesen: '{state.last_page.name}'. "

if quizzes:
    schwach = [q for q in quizzes if q.score < 0.5]
    if schwach:
        kontext += f"Schwache Kapitel: {', '.join(q.page.name for q in schwach)}."
```

---

## Für das Frontend

**Button "Kapitel abschließen" — ruft den Orchestrator auf:**

Der Orchestrator übernimmt den PATCH-Call an unsere API. Das Frontend löst nur den Button-Event aus.

**Nach Abschluss eines Quiz:**
```
POST /api/learning/quiz-results/
{ "page": "<TextbookPage UUID>", "score": 0.8, "attempts": 1 }
```
Falls bereits ein Ergebnis existiert (Update):
```
PATCH /api/learning/quiz-results/{id}/
{ "score": 0.8, "attempts": 2 }
```

---

## Für das KI-Team

Beim Verbindungsaufbau den Nutzerkontext per ORM laden (siehe Orchestrator-Abschnitt oben).

**Beim Disconnect — Gedächtniseintrag schreiben (noch nicht gebaut):**
```python
from openbook.learning.models import MemoryEntry  # noch nicht gebaut

MemoryEntry.objects.create(
    user=self.user,
    course=current_course,
    text="User lernt am besten mit Beispielen. Hat Probleme mit Rekursion."
)
```

---

## Noch offen

- **Tests** — am Ende
- **Signals für Gamification** — nach Absprache mit Lars/Ledejna
- **Quiz-Zuordnung zu Kapitel** — klärt sich mit dem Orchestrator
- **Gedächtniseintrag-Modell** — KI schreibt Notizen über Lernverhalten nach jeder Session
