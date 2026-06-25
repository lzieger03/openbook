# Frontend: Teacher-Bereich – Vollständige Dokumentation

Der Teacher-Bereich ist die **Lehrenden-Oberfläche**: Kurse anlegen/verwalten, Inhalte
(Textbooks & Seiten) schreiben, Skills taggen und Studierende einschreiben. Eigenständiges
Svelte-5-Microfrontend unter `src/frontend/teacher/`.

---

## 1. Technik-Stack

- **Svelte 5** mit Runes, **svelte-spa-router** (Hash-Routing), **Tailwind + daisyUI**.
- **esbuild**-Bundle → `dist/openbook/teacher/bundle.js`, von Django ausgeliefert.
- Einstieg: `src/index.ts` → `initTheme()` → mountet `TeacherApp`.
- Markdown-Vorschau im Editor über `markdown-it`.

---

## 2. Verzeichnisstruktur (`src/frontend/teacher/src/`)

```
index.ts                  Einstieg: Theme + Mount
theme.ts                  Light/Dark-Theme (gemeinsames Muster mit dem Dashboard)
components/
  TeacherApp.svelte       Shell: Header + Router + Footer
  routes.ts               "/" → CourseListPage, "/courses/:id" → CourseDetailPage
  app-frame/
    TeacherHeader.svelte  Marke, Theme-Toggle (Pill), User
  basic/
    Modal.svelte          Wiederverwendbarer Dialog (Slots: children, actions)
  pages/
    CourseListPage.svelte   Kursliste + "New course"-Dialog
    CourseDetailPage.svelte Kurs mit Tabs: Overview / Students / Content
  panels/
    OverviewPanel.svelte    Kursdetails bearbeiten
    StudentsPanel.svelte    Studierende ein-/ausschreiben
    ContentPanel.svelte     Textbooks & Seiten autoren (Kernstück)
stores/
  teacher.store.ts        Lädt die Kurse des aktuellen Lehrenden
api/
  client.ts               apiGet / apiSend (CSRF, Session)
  courses.ts              Kurse + Library-Groups + current_user + slugify
  content.ts              Textbooks, Seiten, Materialien, Page-Ranges, Skills
  enrollment.ts           User-Suche, Student-Rolle, Einschreibungen
  websocket.ts            (gemeinsamer WS-Client, hier kaum genutzt)
data/
  teacher.ts              loadMaterials() → CourseMaterialView (Reihenfolge etc.)
```

---

## 3. Shell, Routing & Store

- **`TeacherApp.svelte`**: Header + gerouteter Inhalt + Footer; abonniert
  `teacherStore` für Name/Avatar im Header.
- **Routen**: `/` = Kursliste, `/courses/:id` = Kursdetail.
- **`teacher.store.ts`**: `refresh()` lädt den aktuellen User und dessen Kurse
  (`fetchCourses(username)`); Status: `isLoading`, `errorMessage`, `user`, `courses`.

---

## 4. API-Schicht (`api/`)

- **`courses.ts`**: `fetchCourses`, `fetchCourse`, `createCourse`, `updateCourse`,
  `deleteCourse`, `fetchLibraryGroups`, `createLibraryGroup`, `fetchCurrentUser`,
  `slugify`. Ein Kurs gehört immer zu einer **Library-Group**.
- **`content.ts`**: `fetchTextbooks`, `createTextbook`, `fetchTextbookPages`,
  `createTextbookPage`, `updateTextbookPage` (jeweils inkl. `skills`-IDs),
  `fetchSkills`, `createSkill`, sowie Materialien:
  `fetchMaterials`, `addMaterial`, `moveMaterial`, `deleteMaterial` und Page-Ranges.
- **`enrollment.ts`**: `searchUsers`, Auflösen/Anlegen der Student-Rolle
  (`STUDENT_ROLE_SLUG = "student"`), `fetchEnrolledStudents`, Ein-/Ausschreiben über
  `role_assignments`.

---

## 5. Datenmodell-Begriffe (wichtig zum Verständnis)

```
Course ──< CourseMaterial >── Textbook ──< TextbookPage >── Skill
   │                                            │
 LibraryGroup                              (Inhalt: MD/HTML/Plaintext)
```

- **Course** lebt in einer **LibraryGroup**.
- **CourseMaterial** verknüpft einen **Textbook** mit dem Kurs (Reihenfolge = Position).
- **TextbookPage** trägt den eigentlichen Inhalt; **Skills** werden **pro Seite**
  zugewiesen (Basis für Quiz-Belohnungen, siehe Gamification-Doku).

---

## 6. Seiten & Panels

### `CourseListPage`
Kurse als Karten (Name, Beschreibung, Materialanzahl, „Manage", „Delete" mit
Bestätigung). **„New course"-Dialog** (in `Modal.svelte`):
- Sichtbar nur die Pflichtangaben: **Kursname** + **Library-Group** (bestehende wählen
  oder neue per Name anlegen).
- Alles Weitere (Slug, Beschreibung, Textformat, „Template course", Group-Slug/Parent/
  Beschreibung) ist unter **„Advanced settings"** eingeklappt – sinnvolle Defaults.

### `CourseDetailPage`
Lädt einen Kurs und zeigt drei Tabs:
- **Overview** (`OverviewPanel`) – Kursdetails bearbeiten/speichern.
- **Students** (`StudentsPanel`) – Studierende suchen und ein-/ausschreiben (Student-
  Rolle im Kurs-Scope).
- **Content** (`ContentPanel`) – Inhalte autoren (siehe unten).

### `ContentPanel` – Inhalte hinzufügen (überarbeitete, einfache UX)
Geführter, geradliniger Ablauf:
1. **Textbook hinzufügen** – ein Eingabefeld „New textbook name" + „+ Add textbook"
   (Enter genügt). Slug/Format werden automatisch gesetzt; das neue Textbook öffnet sich
   direkt.
2. **Bestehendes Textbook anhängen** – als eingeklappte Sekundäroption.
3. Klick auf ein Textbook öffnet einen **Zwei-Spalten-Editor**:
   - **links** die Seitenliste (anklickbar) + „New page"-Feld,
   - **rechts** der Editor: Titel, Format (MD/HTML/Plaintext), **Skill-Tagging**
     (durchsuchbar, inkl. Inline-Anlegen neuer Skills), **Write/Preview**-Tabs,
     **Import file** (`.md/.html/.txt`) und **Save page**.
4. Textbooks lassen sich neu anordnen (↑/↓) und entfernen.

> Ein **Save** einer Seite stößt serverseitig die **RAG-Synchronisation** an
> (`TextbookDocumentSyncService`): Der Textbook-Inhalt wird zu einem `.md`-Dokument
> gerendert, im Assistant indexiert und ist im Student-Dashboard herunterladbar.

---

## 7. Typische Workflows

- **Neuen Kurs anlegen:** CourseList → „New course" → Name + Library-Group → Create.
- **Inhalt schreiben:** Kurs → Tab „Content" → Textbook-Name eingeben → Seiten anlegen →
  Inhalt schreiben → Skills taggen → Save.
- **Skill neu anlegen:** im Skill-Suchfeld einen neuen Namen tippen → „+ Create …".
- **Studierende einschreiben:** Tab „Students" → User suchen → einschreiben.

---

## 8. Bauen & Entwickeln

```
# Dashboard + Teacher gemeinsam im Watch-Modus
npm run start:dashboard-teacher

# Build / Typecheck nur Teacher
cd src/frontend && npm run build:teacher
cd src/frontend/teacher && npx tsc --noEmit
```

Nach Änderungen: **Browser hart neu laden** (Cmd/Ctrl+Shift+R).

---

## 9. Konventionen / Stolperfallen

- **Keine Svelte-Klassennamen nach daisyUI-Komponenten benennen** (z. B. `.status`,
  `.card`, `.badge`) – sonst „lecken" daisyUI-Eigenschaften (etwa `width: 0.5rem`) ins
  Layout. Spezifische Namen verwenden (`status-box`, `course-card` …).
- **Skills hängen an Seiten**, nicht am Kurs/Textbook direkt; die „Skills des Kurses" im
  Dashboard werden serverseitig aus den Seiten-Skills abgeleitet.
- **Nach Merges** im Backend `migrate` nicht vergessen (sonst 500er im Teacher-Content,
  z. B. fehlende `assistantdocument.textbook`-Spalte).
