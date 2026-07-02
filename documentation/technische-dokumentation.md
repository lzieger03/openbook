# OpenBook – Technische Dokumentation

Dieses Dokument gibt den **technischen Gesamtüberblick** über OpenBook: Architektur,
Technologie-Stack, Backend-Apps, Frontends, Datenfluss (Auth, RAG/KI, Realtime,
Gamification) sowie Entwicklung/Betrieb. Es ist die **Einstiegs-Landkarte** und verweist
für Details auf die spezialisierten Dokumente.

> **Vertiefende Detail-Dokus**
> - Lernenden-Frontend → [`frontend-dashboard.md`](frontend-dashboard.md)
> - Lehrenden-Frontend → [`frontend-teacher.md`](frontend-teacher.md)
> - Gamification (Punkte/Level/Streak/Skills) → [`gamification.md`](gamification.md)
> - Fachliche/Domänen-Sicht → [`fachliche-dokumentation.md`](fachliche-dokumentation.md)
> - Offene Punkte & Demo-Grenzen → [`TODOS.md`](TODOS.md)

---

## 1. Architektur in einem Satz

OpenBook ist eine **Django-Webanwendung mit ASGI/WebSockets** (Django Channels) und einem
**KI-Assistenten auf RAG-Basis**, deren Oberflächen als mehrere **eigenständige
Svelte-5-Microfrontends** gebaut und von Django als Static Files ausgeliefert werden.

```
            Browser
   ┌──────────────────────────────────────────────┐
   │  Svelte-Microfrontends (esbuild-Bundles):     │
   │  app · dashboard · teacher · admin            │
   └───────────────┬───────────────┬──────────────┘
        REST (DRF) │               │ WebSocket (chanx/Channels)
                   ▼               ▼
   ┌──────────────────────────────────────────────┐
   │  Django (ASGI via daphne)                     │
   │  Apps: core auth content learning             │
   │        assistant ai gamification              │
   │  Admin: Django + Unfold                        │
   └───────┬───────────────┬──────────────┬────────┘
           │               │              │
      ┌────▼────┐    ┌──────▼──────┐   ┌───▼───────────┐
      │ SQLite  │    │ sqlite-vec  │   │ Redis         │
      │ (Daten) │    │ (Embeddings)│   │ (Channel-Layer)│
      └─────────┘    └─────────────┘   └───────────────┘
                          │
                     ┌────▼─────────┐
                     │ Mistral API  │  (LLM + Embeddings)
                     └──────────────┘
```

---

## 2. Technologie-Stack

### Backend (`src/openbook/`)
- **Django** als Kern-Framework; **ASGI** über **daphne**, klassisch **WSGI** zusätzlich
  vorhanden (`openbook/asgi.py`, `openbook/wsgi.py`).
- **Django Channels** + **chanx** für WebSocket-Consumer (Kurs-Chat, Quiz, Lern-Events).
  Channel-Layer über **Redis** (`channels_redis`).
- **Django REST Framework** + **drf-spectacular** (OpenAPI-Schema/Doku).
- **django-allauth** (Headless) inkl. **SAML**-Provider; lokaler Mock-IdP für die
  Entwicklung. Lokales Signup ist konfigurierbar erlaubt.
- **Django Unfold** als Admin-Theme (eigenes Admin-Bundle, siehe
  [`admin-bundle-loader-fix.md`](admin-bundle-loader-fix.md)).
- **Datenhaltung:** SQLite (Entwicklung). **Embeddings/Vektorsuche** über die
  SQLite-Erweiterung **sqlite-vec** (eigene Vektortabelle, per Migration angelegt).
- **KI/LLM:** **Mistral** (`mistralai`-Client) für Chat-Antworten und Embeddings
  (`mistral-embed`), gekapselt in `assistant/services/llm_client.py` + `rag_client.py`.

### Frontends (`src/frontend/`)
Vier getrennte Bundles, je mit **Svelte 5 (Runes)**, **TypeScript**, **esbuild** und
**Tailwind + daisyUI**. Jedes Bundle wird nach `dist/openbook/<name>/bundle.js` gebaut und
von Django als Static File ausgeliefert.

| Frontend | Zweck |
|---|---|
| `app` | Gemeinsame App-Shell / Login-/Auth-nahe Oberfläche und geteilte Bausteine |
| `dashboard` | **Lernenden-Oberfläche** (Fortschritt, Kurse, Quiz, Chat, Inhalte, Spiele) |
| `teacher` | **Lehrenden-Oberfläche** (Kurse/Inhalte autoren, Skills, Einschreibung) |
| `admin` | Zusatz-Bundle fürs Django-/Unfold-Admin |
| `libraries` (`src/libraries/`) | Geteilte Web-Component-/Library-Bausteine |

---

## 3. Backend-Apps & Verantwortlichkeiten

| App (`openbook/…`) | Verantwortung |
|---|---|
| `core` | Basis-Mixins (UUID, Slug, Text, Audit, Datetime), Sprachen/Site, Media, Management-Commands (`load_initial_data`, **`seed_demo`**) |
| `auth` | Eigenes **User**-Modell, **Group**, **Role/RoleAssignment**, EnrollmentMethod, AccessRequest, **scope-basierte Objektrechte** |
| `content` | **Course**, **LibraryGroup**, **Textbook**, **TextbookPage**, **CourseMaterial** (+ Page-Ranges) – die Inhaltsstruktur |
| `learning` | Lernzustand pro Nutzer/Kurs (`LearningState`: gelesene/abgeschlossene Seiten, Kursabschluss), Lern-Objectives, Quiz-Ergebnisse |
| `assistant` | **RAG-Dokumente** (aus Textbooks gerendert), Chunks + Embeddings, Indexierung, LLM-Anbindung |
| `ai` | **WebSocket-Consumer/Orchestrator** für Kurs-Chat & Quiz (verbindet Frontend ↔ Assistant ↔ Gamification) |
| `gamification` | **Punkte, Level, Streak, Skills, Kursfortschritt**, RewardEventLog, Services & Signals (siehe Detail-Doku) |
| `drf` | Gemeinsame DRF-Bausteine (Flex-Serializer, ViewSet-Mixins, Anonymous-List/Retrieve) |

---

## 4. Datenmodell – die wichtigsten Entitäten

```
LibraryGroup ──< Course ──< CourseMaterial >── Textbook ──< TextbookPage
                  │                                              │
                  │                                          (content JSON,
                  │                                           text_format MD/HTML/TEXT,
                  │                                           skills M2M)
                  │
   Role/RoleAssignment (Scope = Course)        Skill ──< SkillProgress (pro Account)
                  │
User ──< RoleAssignment        AccountProgress (1:1)   CourseProgress (Account×Course)
   │                            AccountStreak (1:1)     LevelThreshold (global)
   └──< LearningState (Account×Course)                  RewardEventLog (Append-only)
```

- **Inhalt:** `TextbookPage.content` ist ein JSON-„Source"-Objekt
  (`{type:"source", format, source}`); das Frontend rendert daraus HTML.
- **Skills** hängen **an Seiten** (nicht direkt am Kurs); die „Skills eines Kurses" werden
  serverseitig aus den Seiten-Skills abgeleitet.
- **Fortschritt/Belohnung** siehe Gamification-Doku (ein einziger Schreibpfad).

---

## 5. Authentifizierung & Berechtigungen

- **Login:** django-allauth (lokal + SAML; Mock-IdP in der Entwicklung). Sessions/CSRF;
  REST-Requests senden Session-Cookie + `X-CSRFToken`.
- **Zwei Ebenen von Rechten:**
  1. **Modell-Level** über **Gruppen** (`Student`, `Teacher` aus `groups.yaml`-Fixture) –
     z. B. dürfen Teacher Kurse/Textbooks/Seiten anlegen/ändern.
  2. **Objekt-Level** über **scope-basierte Rollen**: `Role` + `RoleAssignment` mit
     `scope_type`/`scope_uuid` (z. B. Scope = ein konkreter Kurs). So wird Einschreibung
     und kursbezogene Berechtigung abgebildet.
- Viewsets, die für Lernende offen lesbar sein müssen (z. B. Kursinhalte), nutzen
  `AllowAnonymousListRetrieveViewSetMixin`.

---

## 6. KI-/RAG-Pipeline

1. **Indexierung:** Beim Speichern einer Seite (`TextbookPageViewSet.perform_create/
   perform_update`) rendert `assistant/services/textbook_sync.py` das Textbook zu einem
   `.md`-`AssistantDocument`, zerlegt es in **Chunks**, berechnet **Embeddings**
   (Mistral) und schreibt die **sqlite-vec**-Vektortabelle neu (`_rebuild_index`).
   ⚠️ **Das passiert synchron im Request** → die Teacher-UI wartet (siehe
   [`TODOS.md`](TODOS.md)).
2. **Abfrage:** `LLM_Client.perform_rag_query()` / `retrieve_rag_context()` holt die
   relevantesten Chunks (Vektorsuche) und beantwortet Fragen kurs-scoped im Chat.
3. **Einstieg/Debug:** Management-Command `ask_assistant`, Re-Index über Admin/Viewset.

---

## 7. Realtime / WebSocket

- Endpoint-Muster: `ws(s)://<host>/ws/ai/courses/<course_id>/chat`.
- Nachrichten sind JSON mit `action` + `payload`, **snake_case**.
- **Wichtig:** Der `ChatConsumer` setzt **`camelize = False`**. Sonst würde chanx
  ausgehende Felder camelCasen (`page_id` → `pageId`) und das snake_case-Frontend würde
  Quiz-Punkte/Skills übersehen. (Siehe Memory/Detail-Dokus.)
- Genutzt für: Kurs-Chat, KI-Quiz-Generierung/-Ergebnis, parallele Lern-Events.

---

## 8. Gamification-Schreibpfad (Kurzfassung)

Ein **einziger Schreibpfad**: Ein Service (`award_course_points`, …) schreibt einen
`RewardEventLog`; ein `post_save`-Signal aktualisiert daraus automatisch globales
Punktekonto, Level (`LevelThreshold`) und Streak. Details inkl. Quiz-/Chat-Anbindung,
Anti-Farming und REST-API in [`gamification.md`](gamification.md).

> **Status-Hinweis:** Die **Mini-Spiele** (Memory/Flashcards/Hangman) sind Demo und
> **noch nicht** an die Gamification angebunden (keine Punkte; Begriffe nur aus dem
> Textbook). Siehe [`TODOS.md`](TODOS.md).

---

## 9. Entwicklung & Betrieb

### Lokal starten (Dev)
Wurzel-`package.json` orchestriert die Dienste über `concurrently`:

```sh
npm start                    # redis + django + maildev + mock-saml + frontend + libraries
npm run start:dashboard      # nur Dashboard-Frontend im Watch-Modus
npm run start:dashboard-teacher
```

### Backend
```sh
cd src
python manage.py migrate
python manage.py seed_demo   # befüllt eine testbare DB (User, Kurs, Inhalte, Gamification)
python manage.py runserver
```
- `seed_demo` (in `openbook/core/management/commands/seed_demo.py`) ist idempotent und
  legt Logins, einen Demo-Kurs mit Inhalten, Skills, Level-Schwellen, Einschreibungen und
  Gamification-Fortschritt an. Details in [`../src/README.md`](../src/README.md).
- **Schnellere venv:** Unter Python 3.14 läuft `manage.py` sehr langsam – die
  Python-3.13-venv (`.venv313`) nutzen.

### Frontend bauen / typprüfen
```sh
cd src/frontend && npm run build            # alle Bundles
cd src/frontend && npm run build:teacher    # einzeln
cd src/frontend/teacher && npx tsc --noEmit # Typecheck
```
Nach Frontend-Änderungen **Browser hart neu laden** (Cmd/Ctrl+Shift+R), da Django das
gebaute Bundle als Static File cacht.

### Tests
```sh
cd src && ../.venv313/bin/python manage.py test openbook.gamification openbook.learning
```
Abdeckung u. a. Gamification (Services/Signals/Level/Streak/Reward), Learning, sowie
Quiz-Reward end-to-end über den ChatConsumer.

### API-Doku
OpenAPI via drf-spectacular; Build-Skripte unter `npm run docs:sync-openapi`.

---

## 10. Wichtige Stolperfallen (technisch)

- **Nach jedem Merge `python manage.py migrate`** – häufigste Fehlerquelle sind
  „no such column"-Fehler durch nicht angewendete Migrationen.
- **`ChatConsumer.camelize = False` muss bleiben** (sonst brechen Quiz-Punkte/Skills).
- **Keine Svelte-Klassennamen nach daisyUI-Komponenten** benennen (`.status`, `.card`,
  `.badge` …) – sonst „lecken" daisyUI-Eigenschaften ins Layout.
- **Inhalt speichern lädt lange** = synchrone RAG-Indexierung (kein Bug, siehe §6/TODOS).
- **Admin-Bundle** wird als ES-Module über einen Loader geladen
  ([`admin-bundle-loader-fix.md`](admin-bundle-loader-fix.md)).
