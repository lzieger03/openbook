# OpenBook – Fachliche Dokumentation

Dieses Dokument beschreibt OpenBook aus **fachlicher / inhaltlicher Sicht**: Was ist das
Produkt, für wen, welche fachlichen Begriffe und Funktionen gibt es, und wie sehen die
typischen Abläufe aus. Es richtet sich an alle, die das System **verstehen und bewerten**
wollen, ohne in den Code zu schauen.

> Technische Umsetzung → [`technische-dokumentation.md`](technische-dokumentation.md) ·
> Offene Punkte/Demo-Grenzen → [`TODOS.md`](TODOS.md)

---

## 1. Vision & Zweck

OpenBook ist ein **interaktives Online-Lehrbuch mit KI-Lernbegleiter**. Es verbindet
klassische, von Lehrenden erstellte Kursinhalte mit einem **KI-Assistenten**, der Fragen
zum Stoff beantwortet, sowie mit **spielerischen Lernelementen** (Quiz, Mini-Spiele) und
**Gamification** (Punkte, Level, Streak, Skills). Ziel ist ein Lernerlebnis, das
Lernende **aktiv begleitet** statt nur Inhalte bereitzustellen.

---

## 2. Zielgruppen & Rollen

| Rolle | Beschreibung | Wichtigste Oberfläche |
|---|---|---|
| **Lernende** (Student) | Arbeiten Kursinhalte durch, stellen Fragen, machen Quiz/Spiele, sammeln Punkte | **Dashboard** |
| **Lehrende** (Teacher) | Erstellen Kurse & Inhalte, taggen Skills, schreiben Studierende ein | **Teacher-Bereich** |
| **Administrierende** | Systemverwaltung, Stammdaten, Berechtigungen | **Django-/Unfold-Admin** |

Berechtigungen wirken auf **zwei Ebenen**: allgemeine Rechte über **Gruppen**
(Student/Teacher) und **kursbezogene** Rechte über **Rollen je Kurs** (z. B. Einschreibung
als Student in einen konkreten Kurs).

---

## 3. Fachliche Kernbegriffe

| Begriff | Bedeutung |
|---|---|
| **Library Group** | Ordner/Struktur, in der Kurse und Lehrbücher fachlich gruppiert sind (z. B. Studiengang → Modul) |
| **Course (Kurs)** | Konkretes Angebot für eine Zielgruppe; definiert eine Lesereihenfolge über ein oder mehrere Lehrbücher |
| **Textbook (Lehrbuch)** | Wiederverwendbares Lehrbuch, das von mehreren Kursen genutzt werden kann |
| **Textbook Page (Seite)** | Eigentlicher Inhalt (Markdown/HTML/Text), Baustein eines Lehrbuchs; trägt **Skills** |
| **Course Material** | Verknüpft ein Lehrbuch (ggf. eingeschränkt auf Seitenbereiche) in einen Kurs und legt die Reihenfolge fest |
| **Skill** | Kompetenz aus einem globalen Katalog; wird **pro Seite** zugewiesen und durch Lernen verbessert |
| **Quiz** | KI-generierte Fragen zu einem Lehrbuch; Grundlage für Punkte & Skill-Fortschritt |
| **Gamification** | Punkte, Level, Daily Streak und Skill-Fortschritt als Motivations-/Feedback-Schicht |

---

## 4. Funktionsumfang (fachlich)

### 4.1 Für Lernende (Dashboard)
- **Fortschrittsübersicht:** Punkte, aktuelles **Level** (mit Fortschrittsbalken),
  **Daily Streak**.
- **Meine Kurse:** je Kurs Level, Punkte, Fortschritt und die im Kurs erlernbaren Skills;
  „Next Steps" als priorisierter Leitfaden (Kurs beenden, Skill leveln, Streak halten …).
- **Skill-Matrix:** Radar-Darstellung der eigenen Skill-Level.
- **Bestenliste:** Top-Platzierungen, eigene Position hervorgehoben.
- **Kursinhalte lesen:** seitenweise Lese-Ansicht mit Inhaltsverzeichnis; **Seite als
  erledigt markieren**, **Kurs abschließen**, **Download** (Lehrbuch als `.md`/PDF).
- **Kurs-Chat (KI):** Fragen zum Stoff stellen; der Assistent antwortet **kursbezogen**
  auf Basis der echten Inhalte (RAG). Auch als andockbares Chat-Widget verfügbar.
- **KI-Quiz:** Lehrbuch wählen → Fragen werden generiert → spielen → **Punkte & Skills**
  werden gutgeschrieben.
- **Mini-Spiele:** Spiele-Hub pro Kurs mit **Memory**, **Flashcards** und **Hangman**.

### 4.2 Für Lehrende (Teacher-Bereich)
- **Kurse anlegen/verwalten** (Name + Library Group genügen; Rest mit sinnvollen
  Defaults).
- **Inhalte autoren:** Lehrbücher und Seiten in einem Zwei-Spalten-Editor schreiben
  (Markdown/HTML/Text), Vorschau, **Datei-Import** (`.md/.html/.txt`).
- **Skills taggen:** Seiten mit Skills versehen (durchsuchbar, neue Skills inline
  anlegbar) – Basis für Quiz-Belohnungen.
- **Studierende einschreiben/ausschreiben.**

### 4.3 Lernlogik & Belohnung (fachlich)
- **Punkte** entstehen durch **Quiz** (leistungs- und verbesserungsbasiert, mit
  Anti-Farming), **Kursabschluss** (+200) und **Fragen im Kurs-Chat** (kleine Pauschale
  mit Tageslimit).
- **Level** ergeben sich aus Punkte-Schwellen – **global** und **pro Kurs**.
- **Streak** belohnt regelmäßige Aktivität (tagesbasiert, Zeitzone Europe/Berlin).
- **Skills** steigen mit erreichten Quizpunkten der jeweils getaggten Seiten.

Details zur Mechanik: [`gamification.md`](gamification.md).

---

## 5. Typische Abläufe (User Journeys)

### Lernende:r
1. Einloggen → **Dashboard** zeigt Fortschritt und Kurse.
2. Kurs öffnen → **Inhalte lesen**, Seiten als erledigt markieren.
3. Bei Fragen den **KI-Chat** nutzen.
4. **Quiz** spielen → Punkte/Skills erhalten → Dashboard aktualisiert sich.
5. Optional **Mini-Spiele** zur Wiederholung; **Kurs abschließen** für Bonuspunkte.

### Lehrende:r
1. Einloggen → **Teacher-Bereich**, Kurs anlegen (Name + Library Group).
2. Tab **Content** → Lehrbuch anlegen → Seiten schreiben → **Skills taggen** → speichern.
3. Tab **Students** → Studierende suchen und **einschreiben**.
4. Inhalte stehen Lernenden sofort im Kurs zur Verfügung (inkl. KI-Chat-Wissen).

---

## 6. Fachlicher Status & bewusste Einschränkungen

OpenBook ist **in aktiver Entwicklung**; einige Funktionen sind bewusst noch als **Demo**
eingebaut:

- **Mini-Spiele (Memory/Flashcards/Hangman): Demo, noch nicht vollständig.**
  - Es gibt **noch keine Punkte fürs Spielen** – die Spiele sind (noch) **nicht** mit der
    Gamification verbunden.
  - Memory & Hangman verwenden **nur Begriffe, die bereits im Lehrbuch stehen** – es gibt
    **noch keine KI-generierten** Begriffe/Antwortmöglichkeiten.
- **Inhalte speichern dauert merklich** (Lehrende), weil neue Inhalte **sofort für die
  KI aufbereitet** werden (Indexierung). Das ist erwartetes Verhalten, kein Fehler.

Die vollständige Liste offener Punkte und geplanter Erweiterungen steht in
[`TODOS.md`](TODOS.md).

---

## 7. Abgrenzung

- OpenBook ist **freie Software** (AGPL) und versteht sich als modernes Lern-/
  Lehrsystem mit KI-Begleitung – **mehr** als ein klassisches LMS, aber mit dessen
  Kernfunktionen (Kurse, Inhalte, Einschreibung, Fortschritt).
- Der KI-Assistent arbeitet **inhaltsbasiert** (RAG über die echten Kursinhalte), nicht
  als allgemeiner Chatbot ohne Kursbezug.
