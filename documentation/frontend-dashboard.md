# Frontend: Student-Dashboard – Vollständige Dokumentation

Das Dashboard ist die **Lernenden-Oberfläche**: Fortschritt, Skills, Bestenliste,
Kurse, KI-Quiz, Kurs-Chat und Lerninhalte. Es ist ein eigenständiges Svelte-5-
Microfrontend unter `src/frontend/dashboard/`.

---

## 1. Technik-Stack

- **Svelte 5** mit Runes (`$state`, `$derived`, `$props`, `$effect`).
- **svelte-spa-router** für Hash-Routing.
- **Tailwind + daisyUI** fürs Styling (`tailwind.css` wird vorab gebaut).
- **esbuild** (`bin/frontend/build.js`) bündelt nach
  `dist/openbook/dashboard/bundle.js`; Django liefert das als Static File aus.
- Einstieg: `src/index.ts` → `initTheme()` → mountet `DashboardApp` an `document.body`.

---

## 2. Verzeichnisstruktur (`src/frontend/dashboard/src/`)

```
index.ts                 Einstieg: Theme + Mount
theme.ts                 Light/Dark-Theme (data-theme, localStorage, System-Default)
components/
  DashboardApp.svelte    Shell: Header + Router + Footer + ChatWidget
  routes.ts              Hash-Routen → Page-Komponenten
  app-frame/
    DashboardHeader.svelte  Marke, Theme-Toggle (Pill), Avatar, Status
    ChatWidget.svelte       Schwebendes/andockbares Chat-Fenster
  pages/
    DashboardPage.svelte    Startseite (Panels-Grid)
    QuizPage.svelte         KI-Quiz (Textbook wählen → spielen → Punkte)
    CourseChatPage.svelte   Vollbild-Kurs-Chat
    ContentPage.svelte      Lese-Ansicht der Kursinhalte + Lernfortschritt
    ProfileEditPage.svelte  Profil bearbeiten
  panels/
    StatsPanel.svelte       Punkte/Level/Streak-Kacheln
    LeaderboardPanel.svelte Bestenliste
    SkillMatrixPanel.svelte Skill-Radar
    MyLearningPanel.svelte  Kurse (Level + Skills) + „Next Steps"
  basic/                    ProgressBar, RadarChart, SegmentedTabs, StatTile, LearningRow
stores/
  dashboard.store.ts      Lädt & hält den Dashboard-State
  quiz.store.ts           Quiz über WebSocket
  ai-chat.store.ts        Kurs-Chat über WebSocket
api/
  client.ts               apiGet / apiSend (Basis-URL, CSRF, Session)
  gamification.ts         account_progress, streak, skills, course_progress, leaderboard, current_user
  content.ts              Kursmaterialien, Seiten, Assistant-Dokumente (Download)
  learning.ts             record-page-opened / mark-page-completed / complete-course / fetch state
  assistant.ts, profile.ts, websocket.ts
data/
  dashboard.ts            DTO → View-Modelle für das Dashboard
  course-content.ts       Kursinhalte (Materialien → Seiten → HTML)
  markdown.ts             Gemeinsamer Markdown-Renderer (sicher, html:false)
```

---

## 3. Shell, Routing & Theme

- **`DashboardApp.svelte`**: feste Höhe (`100vh`), Header oben, gerouteter Inhalt in der
  Mitte, Footer unten, dazu das `ChatWidget` (außer auf der `/chat`-Seite). Dockt der
  Chat als Sidebar an, macht die Shell rechts Platz (`padding-right`).
- **`routes.ts`** (Hash-Routen):
  - `/` → `DashboardPage`
  - `/profile` → `ProfileEditPage`
  - `/quiz/:id` → `QuizPage`
  - `/chat/:id` → `CourseChatPage`
  - `/content/:id` → `ContentPage`
- **`theme.ts`**: `data-theme="light|dark"` am Root, gespeichert in `localStorage`,
  Default = System-Farbschema; `toggleTheme()` (Pill-Toggle im Header).

---

## 4. State-Stores

### `dashboard.store.ts`
Einziger zentraler Store für die Startseite. `refresh()` lädt über
`loadDashboardData()` parallel: aktuellen User, AccountProgress, Streak, SkillProgress,
CourseProgress, Leaderboard – und mappt sie zu View-Modellen. Status: `isLoading`,
`errorMessage`, `user`, `stats`, `skills`, `courses`, `leaderboard`.

### `quiz.store.ts`
Quiz-Ablauf über die Kurs-Chat-WebSocket (`/ai/courses/:id/chat`):
- `requestQuiz(count, textbookId)` → sendet `quiz_start`.
- empfängt `quiz_generated` (Fragen + `page_id` als Anker).
- `submitResult(score, attempts)` → sendet `learning_quiz_result`; stellt vorher die
  Verbindung sicher (`connect()`), damit nichts auf einem toten Socket verloren geht.
- Option `onResultRecorded(reward)` → liefert vergebene Punkte/Skills zurück (UI-Feedback).

### `ai-chat.store.ts`
Kurs-Chat (Vollbild & Widget): `sendChatInput`, `getChatHistory`, plus WS-Lernevents
`recordPageOpened` / `markPageCompleted` (parallele WS-Variante; das Dashboard nutzt für
Seiten/Abschluss aber die REST-Endpoints aus `api/learning.ts`).

---

## 5. API-Schicht (`api/`)

- **`client.ts`**: `apiGet(path, query)` und `apiSend(method, path, body)`. Setzt
  `credentials: "include"` (Session-Cookie) und `X-CSRFToken`. Wirft sprechende Fehler.
- **`gamification.ts`**: `fetchAccountProgress` (`/account_progress/me/`),
  `fetchStreak`, `fetchSkillProgress`, `fetchCourseProgress` (`_expand=course`),
  `fetchLeaderboard`, `fetchCurrentUser`.
- **`content.ts`**: `fetchMaterials`, `fetchPageRanges`, `fetchTextbookPages`,
  Assistant-Dokumente inkl. `download_url` (Textbook-Download als `.md`).
- **`learning.ts`**: `recordPageOpened`, `markPageCompleted`, `completeCourse`,
  `fetchLearningState` → Anbindung an das Lernstandsmodell (siehe Gamification-Doku §7).
- **`websocket.ts`**: typsicherer WebSocket-Client mit Reconnect/Backoff und
  action-basiertem Routing. **Protokoll ist snake_case** (passend zum Backend mit
  `camelize = False`).

---

## 6. Daten-/View-Schicht (`data/`)

- **`dashboard.ts`**: wandelt Backend-DTOs in UI-Modelle:
  - `DashboardStats` (Punkte, Level, Level-Fortschritt 0–100, Streak …)
  - `DashboardSkill` (Name, Icon, Level, Progress)
  - `DashboardCourse` (Name, **Level**, Punkte, Progress, **earnable skills**)
  - `DashboardLeaderboardEntry`
  - DecimalFields kommen als String („15.00") und werden geparst.
- **`course-content.ts`**: lädt Materialien → Page-Ranges → Seiten, sortiert in
  Lesereihenfolge, rendert Quell-Inhalt (MD/HTML/Plaintext) zu HTML; liefert zusätzlich
  herunterladbare Assistant-Dokumente pro Material.
- **`markdown.ts`**: `renderMarkdown()` (markdown-it, `html:false`) – sicher fürs
  `{@html}`-Einfügen, genutzt im Chat.

---

## 7. Seiten & Panels

### `DashboardPage`
Titel „@user Dashboard" + zweispaltiges Grid (stapelt < 60rem): links
`MyLearningPanel`, rechts `StatsPanel`, `LeaderboardPanel`, `SkillMatrixPanel`.
Lade-/Fehlerzustand zentriert (`.status-box` – **nicht** `.status`, das kollidiert mit
daisyUI).

### Panels
- **StatsPanel** – Kacheln für Punkte, Level (+ Fortschrittsbalken), Streak; Kacheln
  brechen responsiv um (`auto-fit`).
- **LeaderboardPanel** – Top 10, eigener Eintrag hervorgehoben.
- **SkillMatrixPanel** – Radar-Chart der Skill-Level.
- **MyLearningPanel** – pro Kurs eine Karte mit **Level-Badge** und **Skills**
  (max. 3 Tags + „+N"-Overflow); Tabs „Current / Next Steps / Repeat". „Next Steps" ist
  ein priorisierter Leitfaden aus echten Daten (Kurs beenden, Skill leveln, nächstes
  Level, Streak halten).

### `QuizPage`
Textbook auswählen (zeigt dessen Skills) → Quiz wird per WS generiert → spielen →
Ergebnis. Beim Abschluss `submitResult` → Backend vergibt Punkte/Skills → die
**verdienten Punkte/Skills** werden angezeigt und das Dashboard via `onResultRecorded`
neu geladen.

### `CourseChatPage` & `ChatWidget`
Kurs-Chat über `ai-chat.store`. Assistenten-Antworten mit `format === "markdown"` werden
über `renderMarkdown` **formatiert** dargestellt (`.bubble.md` mit Prose-Styles:
Überschriften, Listen, Code-Blöcke …).

### `ContentPage` – Lese-Ansicht **mit Lernfortschritt**
Inhaltsverzeichnis links, Inhalt rechts. Anbindung ans Lernstandsmodell:
- Seite öffnen → `recordPageOpened` (erste Seite beim Laden + bei TOC-Klick, dedupliziert).
- pro Seite **„Mark complete"** → `markPageCompleted`; erledigte Seiten zeigen ✓.
- am Ende **„Complete course"** → `completeCourse` (Backend vergibt +200 Punkte) →
  danach `dashboardStore.refresh()`. Gespeicherter Fortschritt wird beim Öffnen geladen.
Zusätzlich: **Download-Links** pro Textbook (`.md`, aus den Assistant-Dokumenten).

### `ProfileEditPage`
Profil bearbeiten (`api/profile.ts`).

---

## 8. WebSocket-Protokoll (Kurzfassung)

Endpoint: `ws(s)://<host>/ws/ai/courses/<course_id>/chat`. Nachrichten sind JSON mit
`action` + `payload`, **snake_case**.

Gesendet: `chat_input`, `quiz_start`, `learning_quiz_result`, `learning_page_opened`,
`learning_page_completed`. Empfangen: `chat_message`, `chat_history`, `quiz_generated`,
`learning_event_status` (enthält bei `learning_quiz_result` auch `points_awarded` /
`skills_advanced`).

> Achtung: Das Backend (chanx) hat `camelize = False`. Würde camelCase aktiv sein,
> kämen `page_id` als `pageId` an und das Frontend würde sie übersehen.

---

## 9. Bauen & Entwickeln

```
# nur Dashboard im Watch-Modus (mit Django, Redis, …)
npm run start:dashboard

# Build / Typecheck
cd src/frontend && npm run build:dashboard
cd src/frontend/dashboard && npx tsc --noEmit
```

Nach Frontend-Änderungen: **Browser hart neu laden** (Cmd/Ctrl+Shift+R), da Django das
gebaute Bundle als Static File cacht.
