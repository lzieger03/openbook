# openbook_learning

Verfolgt den Lernfortschritt der Nutzer für den KI-Tutor (ELISA).
Der ChatConsumer liest diese Daten beim WebSocket-Connect und gibt sie als Kontext an das LLM weiter.

---

## Modelle

### LearningState
Eine Zeile pro User+Kurs. Wird aktualisiert sobald der Nutzer eine Seite öffnet.

| Feld           | Typ           | Beschreibung                              |
|----------------|---------------|-------------------------------------------|
| `id`           | UUID          | Primärschlüssel                           |
| `user`         | FK → User     | Der Lernende                              |
| `course`       | FK → Course   | Der Kurs in dem der Nutzer eingeschrieben ist |
| `last_page`    | FK → TextbookPage (nullable) | Zuletzt besuchte Seite    |
| `last_accessed`| DateTimeField | Wird bei jedem Schreibzugriff automatisch aktualisiert |

Constraint: eindeutig pro `user + course`.

### QuizResult
Eine Zeile pro User+Seite. Wird nach jedem Quiz-Versuch aktualisiert (Score wird überschrieben, Versuche hochgezählt).

| Feld          | Typ           | Beschreibung                              |
|---------------|---------------|-------------------------------------------|
| `id`          | UUID          | Primärschlüssel                           |
| `user`        | FK → User     | Der Lernende                              |
| `page`        | FK → TextbookPage | Das Kapitel zu dem das Quiz gehört    |
| `score`       | Float         | Normierter Score 0.0–1.0                  |
| `attempts`    | Integer       | Wie oft das Quiz bereits gemacht wurde    |
| `answered_at` | DateTimeField | Wird bei jedem Schreibzugriff automatisch aktualisiert |

Constraint: eindeutig pro `user + page`.

---

## API Endpoints

Basispfad: `/api/learning/`

| Methode | Endpoint                           | Beschreibung                              |
|---------|------------------------------------|-------------------------------------------|
| GET     | `/api/learning/states/`            | Lernstände des aktuellen Nutzers abrufen  |
| POST    | `/api/learning/states/`            | Neuen Lernstand anlegen                   |
| PATCH   | `/api/learning/states/{id}/`       | Letzte Seite aktualisieren                |
| GET     | `/api/learning/quiz-results/`      | Quiz-Ergebnisse des aktuellen Nutzers abrufen |
| POST    | `/api/learning/quiz-results/`      | Quiz-Ergebnis anlegen                     |
| PATCH   | `/api/learning/quiz-results/{id}/` | Score aktualisieren + Versuche hochzählen |

Alle Endpoints erfordern Authentifizierung. Jeder Nutzer sieht nur seine eigenen Daten.

Vollständige Dokumentation: `http://localhost:8000/api/schema/redoc/`

---

## Für das Frontend

**Wenn der Nutzer eine Kursseite öffnet:**
```
PATCH /api/learning/states/{id}/
{ "last_page": "<TextbookPage UUID>" }
```
Falls noch kein Lernstand für diesen Kurs existiert, zuerst anlegen:
```
POST /api/learning/states/
{ "course": "<Course UUID>", "last_page": "<TextbookPage UUID>" }
```

**Nach Abschluss eines Quiz:**
```
PATCH /api/learning/quiz-results/{id}/
{ "score": 0.8, "attempts": 2 }
```
Falls noch kein Ergebnis für diese Seite existiert:
```
POST /api/learning/quiz-results/
{ "page": "<TextbookPage UUID>", "score": 0.8 }
```

---

## Für das KI-Team 

**Beim WebSocket-Connect** — Nutzerkontext laden und als Prompt-Kontext nutzen:

Nutzerkontext in `consumers/chat.py` beim WebSocket-Connect laden:

```python
from openbook.learning.models import LearningState, QuizResult

state = LearningState.objects.filter(user=self.user).select_related("course", "last_page").first()
quizzes = QuizResult.objects.filter(user=self.user).select_related("page")

# Kontext-String für den LLM-Prompt zusammenbauen
kontext = ""
if state:
    kontext += f"Der Nutzer ist im Kurs '{state.course.name}'. "
    kontext += f"Zuletzt gelesen: '{state.last_page.name}'. "
    kontext += f"Letzter Zugriff: {state.last_accessed.strftime('%d.%m.%Y')}. "

if quizzes:
    schwach = [q for q in quizzes if q.score < 0.5]
    if schwach:
        kontext += f"Schwache Kapitel: {', '.join(q.page.name for q in schwach)}."
```

**Beim WebSocket-Disconnect** — Gedächtniseintrag schreiben (sobald gebaut):

```python
from openbook.learning.models import MemoryEntry  # noch nicht gebaut

# KI fasst ihre Beobachtungen zusammen und speichert sie
MemoryEntry.objects.create(
    user=self.user,
    course=current_course,
    text="User lernt am besten mit Beispielen. Hat Probleme mit Rekursion."
)
# Ältester Eintrag wird automatisch gelöscht wenn Limit erreicht
```

---

## Noch offen / nicht gebaut

### LearningState erweitern 
- `completed_pages` — M2M-Feld für abgeschlossene Kapitel. Wartet auf Entscheidung wie "abgeschlossen" vom Frontend ausgelöst wird.
- `status` — Status des Lernplans: Offen / Vorwissen abgefragt / Lernphase begonnen / Reflexion begonnen / Fertig / Abgebrochen
- `deadline` — Zu erledigen bis (Datum + Uhrzeit)
- `started_at` — Erstmals begonnen an (Datum + Uhrzeit)
- `completed_at` — Abgeschlossen an (Datum + Uhrzeit)
- `pre_knowledge_rating` — Bewertung des Vorwissens vor Kursbeginn
- `post_knowledge_rating` — Bewertung des erworbenen Wissens nach Abschluss
- FK auf Bewertungsraster — setzt voraus dass Bewertungsraster erst gebaut wird

### Gedächtniseintrag
Kurze Notizen der KI über das Lernverhalten des Users. Wird beim Chat-Connect als Kontext mitgegeben.
- `user` — FK auf User (Pflicht)
- `course` — FK auf Course (optional, leer = kursübergreifend)
- `text` — Inhalt des Gedächtniseintrags
- `created/modified` — via CreatedModifiedByMixin
- **Limit:** Maximale Anzahl Einträge pro User+Kurs noch festzulegen

### Sonstiges
- Tests
