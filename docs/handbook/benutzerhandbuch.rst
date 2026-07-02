===========================
Benutzerhandbuch ELISA-AI
===========================

Dieses Handbuch beschreibt die Nutzung von ELISA-AI im aktuellen OpenBook-Projektstand.
Es richtet sich an normale Nutzerinnen und Nutzer und unterscheidet bewusst zwischen
umgesetzten Funktionen, Proof-of-Concept-Funktionen und geplanten Erweiterungen.

.. contents:: Page Content
   :local:


------------
Einleitung
------------

ELISA-AI ist ein interaktiver KI-Lerntutor im OpenBook-Projekt. Der Prototyp verbindet
Kurse, Lernmaterialien, einen kursbezogenen KI-Chat, Quiz- und Exam-Funktionen,
Lernfortschritt sowie erste spielerische Elemente. Ziel ist eine Lernumgebung, in der
Studierende Inhalte verstehen, wiederholen, üben und über ihren eigenen Lernstand
reflektieren können.

ELISA-AI arbeitet nicht als allgemeiner Chatbot neben dem Kurs. Die vorhandene
Implementierung ist auf Kurse, Textbooks, Textbook-Seiten und Assistant-Dokumente
ausgerichtet. Wenn Kursmaterial vorhanden und indexiert ist, kann der Assistant dieses
Material als Kontext für Antworten, Quizfragen und Prüfungsübungen nutzen.

.. warning::

   ELISA-AI ersetzt keine Lehrperson, keine offizielle Musterlösung und keine
   eigenständige Prüfungsvorbereitung. Antworten und automatisch erzeugte Fragen müssen
   kritisch geprüft werden.

Der aktuelle Stand ist ein Proof of Concept. Mehrere zentrale Funktionen sind im Code
vorhanden, unter anderem Dashboard, Kurs-Chat, Inhaltsansicht, Quiz, Exam, Lernstand,
Gamification, Chatverlauf, Teacher-Frontend und einfache Spiele. Andere Teile, etwa
abschließende didaktische Regeln oder vollständige Auswertungen für Lehrende, sind noch
nicht als fertiges Produkt zu verstehen.


------------------------------
Zielgruppen Dieses Handbuchs
------------------------------

Dieses Handbuch ist für drei Gruppen geschrieben. Studierende finden vor allem in der
Anleitung für Studierende, im Kapitel zu guten Fragen an ELISA und in der FAQ praktische
Hinweise. Lehrende finden in der Anleitung für Lehrende, im typischen Ablauf und im
Kapitel zu verantwortungsvoller Nutzung die wichtigsten Informationen.

Administrierende werden nur am Rand behandelt. OpenBook enthält ein Rollen-,
Berechtigungs- und Administrationskonzept, aber dieses Handbuch beschreibt keine
Installation, Serverwartung oder technische Administration. Dafür sind die
Administrations- und Entwicklerdokumente des Projekts zuständig.

.. note::

   Wenn eine Funktion im aktuellen Repository nur als Konzept oder PoC erkennbar ist,
   wird sie in diesem Handbuch entsprechend markiert. Es werden keine Bedienwege
   beschrieben, die nicht in vorhandener Dokumentation oder im Code erkennbar sind.

**Für Studierende relevant** sind besonders Dashboard, Kursauswahl, Skriptansicht,
KI-Chat, Quiz, Exam, Spiele, Lernfortschritt und Gamification.

**Für Lehrende relevant** sind besonders Kursliste, Kursdetailseite, Content-Bereich,
Studierendenverwaltung, Skill-Tagging, Materialimport und der didaktische Umgang mit
KI-generierten Inhalten.

**Für Administrierende relevant** sind vor allem Anmeldung, Rollen, Berechtigungen und
Systemzustand. Diese Themen werden hier nur aus Nutzersicht erwähnt.


--------------------------------
Grundidee Und Funktionsumfang
--------------------------------

ELISA-AI erweitert OpenBook um eine lernbegleitende Oberfläche. Studierende sollen
nicht nur statische Materialien lesen, sondern mit einem KI-Tutor, Lernpfaden,
Quizfragen und spielerischen Formaten aktiv arbeiten. OpenBook bleibt dabei die
Grundlage für Kurse, Rollen, Textbooks und Seiten.

Der umgesetzte Prototyp besteht aus mehreren sichtbaren Bereichen. Das Student Dashboard
zeigt Lernübersicht, Statistiken, Kurse, Skills, Bestenliste und Navigation zu
Kursfunktionen. Der Kurs-Chat ist ein vollflächiger KI-Chat für einen konkreten Kurs.
Die Inhaltsansicht zeigt Textbook-Seiten, Fortschritt pro Seite und Download-Funktionen.
Quiz und Exam nutzen den kursbezogenen Assistant-Kontext.

**Chat mit ELISA** ist im Dashboard als Kurs-Chat und als Chat-Widget vorgesehen. Der
Chat läuft über einen WebSocket-Kanal für den gewählten Kurs. Der Code enthält außerdem
gespeicherte Chat-Sitzungen mit Chatverlauf, Umbenennen und Löschen von Chats.

**Kursbezogene Inhalte und Materialien** werden über OpenBook-Kurse, Textbooks und
Textbook-Seiten abgebildet. Lehrende können im Teacher-Frontend Inhalte erstellen,
hochladen, importieren, strukturieren und mit Skills versehen. Beim Speichern oder
Importieren können Inhalte für den Assistant synchronisiert werden.

**Lernpfade und Lerneinheiten** sind im aktuellen Code vor allem über Kurse, Textbooks,
Seiten und Lernfortschritt sichtbar. Ein vollständiger, didaktisch ausformulierter
Lernplan ist als Zielbild erkennbar, aber nicht als vollständig fertige
Nutzeroberfläche dokumentiert.

**Quiz und Lernkontrollen** sind umgesetzt. Im Dashboard wählen Studierende ein Textbook
aus, ELISA generiert Fragen für den Kurskontext und die Antworten werden serverseitig
bewertet. Die Oberfläche zeigt Ergebnis, Punkte und Skill-Fortschritt, wenn der Server
diese Werte zurückmeldet.

**Lernfortschritt und Lernstand** sind umgesetzt. Das Modell ``LearningState`` speichert
für angemeldete Nutzer den Kurs, die zuletzt geöffnete Seite, abgeschlossene Seiten,
Kursabschluss und den letzten Zugriff. ``QuizResult`` speichert Quiz-Ergebnisse pro
Nutzer und Seite.

**Gamification** ist im Code und in der Dokumentation breit umgesetzt. Dazu gehören
globale Punkte, Kursfortschritt, Level, Daily Streaks, Skills, Skill-Fortschritt,
Rewards, Reward-Events und Leaderboard. Die konkreten pädagogischen Regeln sind im
Proof of Concept noch nicht abschließend als Produktregelwerk zu verstehen.

**Interaktive Spiele** sind im Dashboard vorhanden. Es gibt eine Games-Seite sowie
Routen für Memory, Flashcards und Hangman. Diese Spiele nutzen, soweit möglich,
Begriffe und Inhalte aus dem Kurs. Sie sind als PoC-Lernformate einzuordnen.


---------------
Rollenmodell
---------------

ELISA-AI arbeitet mit unterschiedlichen Rollen. Für normale Nutzerinnen und Nutzer ist
wichtig, welche Aufgaben mit welcher Rolle verbunden sind. Die technische
Berechtigungslogik bleibt im Hintergrund.

Studierende nutzen ELISA-AI zum Lernen. Sie öffnen Kurse, lesen Inhalte, stellen Fragen,
starten Quiz- oder Exam-Übungen, spielen einfache Lernspiele und sehen Fortschritt,
Punkte, Skills, Level und Streaks.

Lehrende bereiten Kurse und Inhalte vor. Sie legen Kurse an, verwalten Textbooks und
Seiten, importieren Materialien, vergeben Skills pro Seite und schreiben Studierende in
Kurse ein oder aus. Außerdem entscheiden sie, wie KI-Chat, Quiz und Spiele didaktisch
eingesetzt werden.

Administrierende verwalten Benutzer, Rollen und Systemkonfiguration im OpenBook-Kontext.
Im aktuellen ELISA-Benutzerhandbuch wird diese Rolle nur allgemein erwähnt, weil die
Administration nicht Teil der eigentlichen Lernoberfläche ist.

.. graphviz::
   :caption: Rollen und typische Aufgaben in ELISA-AI
   :align: center

   digraph rollen {
      graph [bgcolor=transparent];
      rankdir=LR;
      node [shape=box, style="rounded,filled", fillcolor="#f8fafc", color="#64748b"];
      edge [color="#475569"];

      student [label="Studierende"];
      teacher [label="Lehrende"];
      admin [label="Administration"];
      elisa [label="ELISA-AI"];

      student -> elisa [label="Fragen stellen\nQuiz/Spiele nutzen\nLernfortschritt ansehen"];
      teacher -> elisa [label="Kurse verwalten\nMaterialien bereitstellen\nLernformate vorbereiten"];
      admin -> elisa [label="Benutzer und Rollen verwalten"];
   }


----------------
Erste Schritte
----------------

ELISA-AI ist Teil von OpenBook. Der Einstieg hängt davon ab, welche Oberfläche in der
jeweiligen Umgebung gestartet wurde. Im aktuellen Code gibt es eine allgemeine
OpenBook-App, ein Student Dashboard und ein Teacher-Frontend. Die ELISA-Funktionen
liegen vor allem im Dashboard und im Teacher-Frontend.

**Anwendung öffnen** --- Öffnen Sie die bereitgestellte OpenBook-Adresse im Browser.
Für den Prototyp können je nach Umgebung unterschiedliche Startadressen verwendet
werden. Entscheidend ist, dass Sie in der passenden Oberfläche landen: Student
Dashboard für Lernende oder Teacher-Frontend für Lehrende.

**Anmelden** --- Der WebSocket-Chat und die Lernstands-Endpunkte setzen einen
angemeldeten Nutzer voraus. Ohne Login können Chat, Lernfortschritt, Quiz-Ergebnisse
und kursbezogene Daten nicht zuverlässig geladen oder gespeichert werden.

**Kurs auswählen** --- Studierende sehen ihre Kurse im Dashboard. Lehrende sehen ihre
Kurse in der Teacher-Kursliste. Wenn kein Kurs erscheint, ist wahrscheinlich noch keine
Einschreibung, kein Kurs oder keine passende Berechtigung vorhanden.

**Startseite verstehen** --- Im Student Dashboard erscheinen Lernübersicht, Statistik,
Leaderboard und Skill-Matrix. Im Teacher-Frontend erscheinen Kurskarten mit
Kursstatus, Anzahl der Textbooks und Skills.

.. note::

   Login, Kursauswahl und Rollen hängen im PoC von der lokalen OpenBook-Einrichtung ab.
   Wenn Testdaten, Migrationen oder Rollen fehlen, können sichtbare Funktionen leer
   bleiben oder Fehlermeldungen anzeigen.

Screenshots sind im aktuellen Repository für dieses Handbuch nicht als eigene
Benutzerhandbuch-Grafiken hinterlegt. Sie können später ergänzt werden, sobald ein
stabiler Demo-Stand festgelegt ist.


----------------------------
Anleitung Für Studierende
----------------------------

Studierende arbeiten im Normalfall im Student Dashboard. Von dort führen die
Kurskarten in den Kurs-Chat. In der Chat-Seitenleiste sind weitere Bereiche erreichbar:
Skript, Games, Quizzes, Exams und gespeicherte Chats.

Kurs Auswählen
..............

Öffnen Sie das Student Dashboard. In der Lernübersicht werden die Kurse angezeigt, die
für Ihren Account geladen werden können. Ein Klick auf einen Kurs öffnet im aktuellen
Dashboard den Kurs-Chat.

Wenn ein Kurs fehlt, prüfen Sie zuerst, ob Sie angemeldet sind. Danach muss geprüft
werden, ob Sie im Kurs eingeschrieben sind. Im PoC kann die Einschreibung über das
Teacher-Frontend oder über Rollen im OpenBook-System vorbereitet werden.

Dashboard Und Lernübersicht Verstehen
......................................

Das Dashboard zeigt mehrere Bereiche. ``MyLearningPanel`` listet Kurse und nächste
Schritte. ``StatsPanel`` zeigt Punkte, Level und Streak. ``LeaderboardPanel`` zeigt eine
Bestenliste. ``SkillMatrixPanel`` zeigt Skill-Fortschritt als Übersicht.

Diese Werte sind Orientierungshilfen. Sie zeigen Aktivität und Fortschritt, ersetzen
aber keine fachliche Rückmeldung durch Lehrende. Besonders Punkte und Streaks sollen
regelmäßiges Lernen unterstützen, nicht allein Leistung bewerten.

.. admonition:: Tipp

   Nutzen Sie das Dashboard als Startpunkt: Kurs öffnen, Material lesen, Frage stellen,
   Quiz bearbeiten und danach prüfen, ob sich Fortschritt, Punkte oder Skills geändert
   haben.

Lernpfad Und Lerneinheiten Nutzen
.................................

Im Kurs-Chat führt der Button ``Skript`` zur Inhaltsansicht. Dort sehen Sie links ein
Inhaltsverzeichnis und rechts die aktuelle Textbook-Seite. Sie können Seiten direkt
auswählen oder mit ``Previous`` und ``Next`` durch den Kurs gehen.

Wenn Sie eine Seite öffnen, meldet die Oberfläche diesen Zugriff an den Lernstand.
Wenn Sie eine Seite abgeschlossen haben, können Sie sie mit ``Mark complete`` markieren.
Am Ende des Kurses kann ``Complete course`` den Kursabschluss speichern.

.. note::

   Der Lernpfad ist im aktuellen Prototyp vor allem eine strukturierte Abfolge von
   Textbook-Seiten. Ein vollständig adaptiver Lernplan ist als Zielbild beschrieben,
   aber nicht als fertige Nutzeroberfläche belegt.

Fragen An ELISA Stellen
.......................

Der Kurs-Chat ist für Fragen zum ausgewählten Kurs gedacht. Geben Sie Ihre Frage in das
Eingabefeld ein und senden Sie sie ab. Der Chat zeigt den Verbindungsstatus an. Nur bei
aktiver Verbindung kann eine Nachricht gesendet werden.

Gespeicherte Chat-Sitzungen erscheinen in der Chat-Seitenleiste. Sie können einen neuen
Chat starten, vorhandene Chats öffnen, umbenennen oder löschen. So lassen sich mehrere
Lernkontexte pro Kurs getrennt halten.

Antworten Richtig Einordnen
............................

ELISA kann Markdown-Antworten anzeigen und Kurskontext verwenden. Trotzdem können
Antworten falsch, unvollständig oder missverständlich sein. Prüfen Sie wichtige
Informationen mit den Kursmaterialien und den Vorgaben Ihrer Lehrperson.

.. warning::

   Übernehmen Sie keine KI-Antwort ungeprüft in Abgaben, Prüfungen oder
   prüfungsrelevante Notizen. ELISA-AI ist eine Lernhilfe, keine verbindliche
   Autorität.

Quiz Starten Und Bearbeiten
............................

Öffnen Sie im Kurs-Chat den Bereich ``Quizzes``. Wählen Sie zuerst ein Textbook aus.
Das Quiz wird danach für dieses Textbook und den aktuellen Kurs generiert. Wenn keine
Textbooks vorhanden sind, zeigt die Oberfläche einen entsprechenden Hinweis.

Das Quiz besteht aus Multiple-Choice-Fragen. Wählen Sie pro Frage eine Antwort aus. Nach
dem Durchlauf werden Ihre Antworten serverseitig bewertet und das Ergebnis wird
angezeigt. Über ``Try again``, ``New quiz`` oder ``Change textbook`` können Sie weiter
üben.

Feedback Nach Quizfragen Verstehen
..................................

Nach dem Quiz zeigt die Oberfläche Ihr Ergebnis als Anzahl korrekter Antworten. Wenn
der Server Punkte oder Skill-Fortschritt vergibt, werden diese Werte direkt im Ergebnis
angezeigt und das Dashboard wird aktualisiert.

Das Gamification-System vergibt Quizpunkte verbesserungsbasiert. Ein erneuter Versuch
mit gleichem oder niedrigerem Ergebnis kann daher keine neuen Punkte bringen. Das ist
als Anti-Farming-Regel im PoC umgesetzt.

Lernfortschritt, Punkte, Skillpoints, Level Und Streaks Verstehen
.................................................................

Der Lernfortschritt wird auf mehreren Ebenen sichtbar. Abgeschlossene Seiten erscheinen
in der Inhaltsansicht. Der zuletzt besuchte Stand wird im Modell gespeichert. Der
Kursabschluss kann zusätzliche Kurspunkte vergeben.

Punkte und Level existieren global und pro Kurs. Skills haben einen eigenen Fortschritt
pro Nutzer. Streaks zeigen regelmäßige Lernaktivität. Das System erfasst etwa
Seitenaufrufe, Quiz-Ergebnisse, Chat-Fragen und Kursabschluss unterschiedlich.

.. admonition:: Tipp

   Verstehen Sie Punkte als Lernmotivation. Ein hoher Punktestand bedeutet nicht
   automatisch, dass Sie ein Thema sicher beherrschen. Nutzen Sie zusätzlich Quiz,
   eigene Erklärungen und Rückfragen.

Interaktive Spiele Nutzen
..........................

Öffnen Sie im Kurs-Chat den Bereich ``Games``. Dort sind Memory, Flashcards und Hangman
verfügbar. Die Spiele nutzen nach Möglichkeit Begriffe, Überschriften und Inhalte aus
dem Kurs. Wenn keine passenden Kursdaten vorhanden sind, können sie mit neutralen
Fallback-Inhalten arbeiten oder leer bleiben.

Memory lässt Sie Begriffspaare finden. Flashcards zeigen Karten mit Vorder- und
Rückseite aus Kursinhalten. Hangman nutzt Fachbegriffe aus den Textbook-Seiten. Diese
Spiele sind PoC-Lernformate und sollten als Übungsergänzung verstanden werden.

Typische Nutzungsszenarien
..........................

**Unklaren Abschnitt verstehen** --- Öffnen Sie die Kursseite, lesen Sie den Abschnitt
und fragen Sie ELISA gezielt nach dem Teil, der unklar ist. Lassen Sie sich danach ein
Beispiel oder Gegenbeispiel geben.

**Vor einer Präsenzveranstaltung wiederholen** --- Öffnen Sie den Kurs, markieren Sie
bearbeitete Seiten, starten Sie ein Quiz und notieren Sie Fragen, die Sie mit der
Lehrperson klären möchten.

**Begriffe üben** --- Nutzen Sie Flashcards oder Hangman, wenn ein Kurs genügend
Begriffe und Seiten enthält. Prüfen Sie anschließend im Skript, ob Sie die Begriffe
nicht nur wiedererkennen, sondern erklären können.


-------------------------
Anleitung Für Lehrende
-------------------------

Lehrende arbeiten im Teacher-Frontend. Dort können sie Kurse vorbereiten,
Kursmaterialien erstellen oder importieren, Seiten bearbeiten, Skills vergeben und
Studierende einschreiben. Die Oberfläche ist als einfachere Alternative zu reinem
Django-Admin-Arbeiten gedacht.

Kurs Vorbereiten
................

Öffnen Sie das Teacher-Frontend. Die Startseite zeigt ``My Courses`` mit vorhandenen
Kursen. Über ``New course`` legen Sie einen neuen Kurs an. Dazu benötigen Sie mindestens
einen Kursnamen und eine Library Group.

Sie können eine vorhandene Library Group auswählen oder eine neue erstellen. Weitere
Einstellungen wie Slug, Beschreibung, Textformat oder Template-Status liegen im Bereich
``Advanced settings``. Für normale Kursarbeit reichen die Pflichtangaben meist aus.

Materialien Bereitstellen Oder Hochladen
........................................

Öffnen Sie einen Kurs und wechseln Sie zum Tab ``Content``. Dort können Sie ein neues
Textbook über einen Namen anlegen oder ein vorhandenes Textbook anhängen. Zusätzlich
ist ein Upload für Skripte vorgesehen.

Der Materialimport akzeptiert laut Backend ``.md``, ``.markdown``, ``.html``, ``.htm``,
``.txt`` und ``.pdf``. Bei Uploads versucht das Backend, Kapitel zu erkennen und daraus
Textbook-Seiten anzulegen. Nach dem Import kann das Material im Editor geprüft und
überarbeitet werden.

.. warning::

   Prüfen Sie importierte Materialien immer. Automatische Kapiteltrennung und
   Markdown-/PDF-Extraktion können unvollständig sein oder Nacharbeit erfordern.

Inhalte Strukturieren
.....................

Ein Kurs enthält Textbooks, und Textbooks enthalten Seiten. Im Content-Bereich können
Sie Textbooks öffnen, Seiten anlegen, Seiten löschen, Seiteninhalte schreiben und eine
Vorschau anzeigen. Seiten können in Markdown, HTML oder Plain Text gepflegt werden.

Skills werden im aktuellen Modell pro Textbook-Seite vergeben. Diese Skills bilden die
Grundlage dafür, welche Fähigkeiten im Dashboard und bei Quiz-Belohnungen sichtbar
werden. Neue Skills können direkt im Skill-Suchfeld angelegt und einer Seite zugeordnet
werden.

Lernformate Aktivieren Oder Vorbereiten
.......................................

Quiz, Exam, Spiele und KI-Chat hängen stark davon ab, ob Kursinhalte vorhanden und
sinnvoll strukturiert sind. Legen Sie daher aussagekräftige Seiten an, benennen Sie
Kapitel klar und vergeben Sie Skills nur dort, wo sie fachlich passen.

Beim Speichern von Seiten oder beim Import von Textbooks kann das System den Inhalt als
Assistant-Dokument synchronisieren. Dadurch kann der Assistant Kursmaterial als Kontext
verwenden. Der Indexstatus kann technisch relevant sein, ist aber im normalen
Lehrendenablauf vor allem dann wichtig, wenn der Assistant Material nicht berücksichtigt.

Quiz Und Lernkontrollen Einsetzen
.................................

Studierende starten Quizze selbst im Dashboard. Lehrende bereiten dafür indirekt die
Grundlage: Textbooks, Seiten, Skills und Kursmaterialien. Das Quiz wird aus
RAG-Dokumenten oder aus dem Kurskontext erzeugt und serverseitig bewertet.

Exams sind ebenfalls im Dashboard vorhanden. Sie erzeugen und bewerten
prüfungstypische Aufgaben im Kurskontext. Da KI-generierte Aufgaben und Bewertungen
fehlerhaft sein können, sollten Exams im PoC nur als Übung und Reflexionshilfe genutzt
werden.

Lernstand Und Auswertungen
..........................

Der Code enthält Lernstandsdaten, Quiz-Ergebnisse, Kursfortschritt, Skill-Fortschritt,
Streaks und Reward-Events. Daraus lassen sich grundsätzlich Fortschritt und Aktivität
ableiten. Das Dashboard zeigt diese Daten vor allem für Studierende.

Ein fertiges, datenschutzfreundliches Reporting für Lehrende ist im aktuellen Stand
nicht als abgeschlossenes Produkt dokumentiert. Lehrende sollten daher keine
personenbezogene Leistungsbewertung aus ELISA-Daten ableiten, solange kein klares
pädagogisches und rechtliches Auswertungskonzept festgelegt ist.

Didaktische Hinweise Zur Nutzung Im Selbststudium
.................................................

ELISA-AI eignet sich besonders für betreutes Selbststudium. Studierende können Inhalte
vorbereiten, Verständnisfragen stellen, Quizze bearbeiten und offene Punkte in die
Präsenzveranstaltung mitbringen. Dadurch kann Präsenzzeit stärker für Diskussion,
Übung und Feedback genutzt werden.

Geben Sie Studierenden klare Regeln. Legen Sie fest, wann KI-Unterstützung erlaubt ist,
wie Antworten geprüft werden sollen und welche Nutzung in Abgaben nicht zulässig ist.
Eine gute Regel ist: ELISA darf beim Verstehen helfen, aber nicht das eigene Denken
ersetzen.

Grenzen Aus Lehrendensicht
..........................

Der Prototyp ist nicht mit einem vollständigen Lernmanagementsystem gleichzusetzen.
Einige Oberflächen und Dienste sind vorhanden, aber nicht alle Workflows sind final
stabilisiert. Insbesondere Bewertung, Reporting, finale Gamification-Regeln und
produktive Qualitätssicherung brauchen weitere fachliche Entscheidungen.

Nutzen Sie KI-generierte Quizfragen, Exam-Feedback und Assistant-Antworten nicht als
ungeprüfte Musterlösung. Prüfen Sie fachliche Richtigkeit, didaktische Passung und
Datenschutz, bevor Sie Ergebnisse in formalen Lehrkontexten einsetzen.


-----------------------------
Typischer Nutzungsablauf
-----------------------------

Ein typischer Ablauf aus Studierendensicht beginnt mit der Anmeldung und Kursauswahl.
Danach lesen Studierende Kursinhalte, stellen Fragen an ELISA, bearbeiten ein Quiz oder
eine Lernaktivität und sehen anschließend Feedback sowie Fortschritt.

Aus Lehrendensicht beginnt der Ablauf mit einem Kurs. Lehrende erstellen oder wählen
eine Library Group, legen Textbooks und Seiten an, importieren Material, vergeben Skills
und schreiben Studierende ein. Danach können Studierende mit dem Kurs arbeiten.

.. graphviz::
   :caption: Vereinfachter Nutzungsablauf von ELISA-AI
   :align: center

   digraph ablauf {
      graph [bgcolor=transparent];
      rankdir=TB;
      node [shape=box, style="rounded,filled", fillcolor="#f8fafc", color="#64748b"];
      edge [arrowsize=0.8, color="#475569"];

      start [label="Anmeldung"];
      course [label="Kurs auswählen"];
      content [label="Lerninhalt öffnen"];
      chat [label="Frage an ELISA stellen"];
      quiz [label="Quiz oder Lernaktivität starten"];
      feedback [label="Feedback erhalten"];
      progress [label="Lernfortschritt aktualisieren"];

      start -> course;
      course -> content;
      content -> chat;
      chat -> quiz;
      quiz -> feedback;
      feedback -> progress;
   }

**Studierendenablauf**:

1. Im Browser anmelden.
2. Student Dashboard öffnen.
3. Kurs auswählen.
4. Im Kurs-Chat eine Frage stellen oder über ``Skript`` die Inhalte öffnen.
5. Seiten lesen und mit ``Mark complete`` abschließen.
6. Quiz, Exam oder Spiel starten.
7. Feedback, Punkte, Skills und Fortschritt prüfen.

**Lehrendenablauf**:

1. Im Teacher-Frontend anmelden.
2. Kurs anlegen oder bestehenden Kurs öffnen.
3. Textbook anlegen, vorhandenes Textbook anhängen oder Material hochladen.
4. Seiten strukturieren und Inhalte prüfen.
5. Skills pro Seite vergeben.
6. Studierende einschreiben.
7. KI- und Quiz-Nutzung didaktisch erklären.


--------------------------------
Gute Fragen An ELISA Stellen
--------------------------------

Gute Fragen sind konkret. Nennen Sie das Thema, den Abschnitt oder den Begriff, mit dem
Sie arbeiten. Beschreiben Sie außerdem, was Sie nicht verstehen oder was Sie überprüfen
möchten.

Beispiele für sinnvolle Fragen:

* "Erkläre mir das Thema in einfachen Worten."
* "Stelle mir drei Verständnisfragen zu diesem Abschnitt."
* "Prüfe, ob ich den Unterschied zwischen X und Y verstanden habe."
* "Gib mir ein Beispiel aus der Praxis."
* "Welche Begriffe aus dieser Seite sollte ich wiederholen?"
* "Fasse diesen Abschnitt als Lernkarte zusammen."

.. admonition:: Tipp

   Eine gute Frage an ELISA enthält Kontext und ein Ziel. Besser als "Erkläre alles" ist
   zum Beispiel: "Erkläre mir den Unterschied zwischen synchroner und asynchroner
   Kommunikation anhand eines Beispiels."

Schlechte Nutzungsweisen schwächen den Lerneffekt. Dazu gehört, eine Lösung ohne
eigenes Nachdenken zu übernehmen, prüfungsrelevante Inhalte ungeprüft zu kopieren oder
ELISA nach endgültigen Antworten für Aufgaben zu fragen, die selbst bearbeitet werden
sollen.

Geben Sie keine privaten oder personenbezogenen Daten in den Chat ein. Dazu gehören
Adressen, Telefonnummern, private Konflikte, Gesundheitsdaten, personenbezogene
Leistungsdaten anderer Personen oder vertrauliche Hochschulunterlagen.


----------------------------------------------
Datenschutz Und Verantwortungsvolle Nutzung
----------------------------------------------

ELISA-AI ist ein KI-System und kann Fehler machen. Antworten können überzeugend
klingen, obwohl sie fachlich nicht stimmen. KI-generierte Quizfragen können
unvollständig, zu leicht, zu schwer oder missverständlich sein.

Prüfen Sie wichtige Antworten mit Kursmaterialien, Lehrendenhinweisen und anerkannten
Quellen. Nutzen Sie ELISA, um Verständnis aufzubauen, nicht um Verantwortung abzugeben.
Bei Widersprüchen gilt nicht automatisch die KI-Antwort.

.. warning::

   Geben Sie keine sensiblen personenbezogenen Daten in den Chat ein. Behandeln Sie
   Chatverläufe und Lernstandsdaten so, als könnten sie technisch gespeichert und im
   vorgesehenen Systemrahmen verarbeitet werden.

Lernstandsdaten sollen nur für den vorgesehenen Zweck verwendet werden. Im aktuellen
Prototyp sind Lernstände, Quiz-Ergebnisse und Gamification-Daten als Lernhilfe und
technische Grundlage sichtbar. Eine automatische Notenvergabe ist nicht dokumentiert
und sollte nicht behauptet oder aus den Daten abgeleitet werden.

Lehrende sollten ELISA-Ergebnisse nicht als alleinige Leistungsbewertung nutzen.
KI-generierte Inhalte sind Lernhilfe, Übungsanstoß und Gesprächsgrundlage, aber keine
verbindliche Musterlösung.


--------------------------------
Grenzen Des Prototyps / PoC
--------------------------------

ELISA-AI ist im aktuellen Repository ein Proof of Concept. Der Code enthält viele
funktionierende Bausteine, aber das System ist noch nicht als vollständig produktionsreife
Lernplattform dokumentiert. Besonders lokale Einrichtung, Migrationen, Frontend-Builds
und Assistant-Abhängigkeiten beeinflussen, ob alle Funktionen in einer Umgebung sichtbar
sind.

Bekannte Grenzen aus Dokumentation und Code:

* Die finale Quiz-Architektur ist fachlich noch zu entscheiden. Der aktuelle Weg läuft
  über den kursbezogenen Assistant-WebSocket.
* Gamification-Regeln sind teilweise umgesetzt, aber pädagogisch noch nicht vollständig
  finalisiert.
* Ein vollständiges Teacher-Reporting ist nicht als fertiger Workflow dokumentiert.
* Lernpfade sind im PoC vor allem über Kursinhalte, Seiten und Fortschrittsdaten
  sichtbar. Ein vollständig adaptiver Lernplan bleibt Zielbild.
* Memory, Flashcards und Hangman sind als einfache PoC-Lernspiele vorhanden.
* Eine vollständige LMS-, Moodle- oder LTI-Integration ist in den betrachteten
  Unterlagen nicht als umgesetzt erkennbar.
* Das Rechte- und Rollensystem basiert auf OpenBook, aber der ELISA-Demo-Workflow kann
  je nach lokaler Testumgebung unvollständig konfiguriert sein.
* Eine vollständige Hochverfügbarkeits- oder Produktionsbetriebsbeschreibung gehört
  nicht zum Benutzerhandbuch und ist für den PoC nicht belegt.
* Assistant-Antworten und KI-generierte Prüfungsübungen brauchen menschliche Prüfung.

Diese Grenzen sind kein Bedienfehler. Sie markieren den aktuellen Projektstand und
helfen, Erwartungen an die Demo und an spätere Projektphasen realistisch zu halten.


----------------------
Fehlerbehebung / FAQ
----------------------

Die folgenden Hinweise beschreiben typische Probleme aus Nutzersicht. In einer lokalen
PoC-Umgebung können technische Ursachen zusätzlich durch fehlende Migrationen,
fehlende Testdaten, nicht gebaute Frontends oder nicht verfügbare Assistant-Abhängigkeiten
entstehen.

**Ich kann mich nicht anmelden. Was kann ich tun?** --- Prüfen Sie Benutzername,
Passwort und die richtige OpenBook-Adresse. Wenn die Anmeldung weiter fehlschlägt,
wenden Sie sich an die betreuende Person oder Administration. Ohne Login funktionieren
Chat, Lernfortschritt und kursbezogene Daten nicht vollständig.

**Ich sehe keinen Kurs.** --- Sie sind möglicherweise nicht in einen Kurs eingeschrieben
oder der Kurs wurde noch nicht angelegt. Lehrende können im Teacher-Frontend Kurse
anlegen und Studierende im Tab ``Students`` einschreiben.

**ELISA beantwortet meine Frage nicht passend.** --- Formulieren Sie die Frage
konkreter und nennen Sie Kurs, Thema oder Abschnitt. Prüfen Sie außerdem, ob im Kurs
Material vorhanden ist. Wenn keine passenden Assistant-Dokumente indexiert sind, kann
ELISA weniger kursbezogen antworten.

**Das Quiz startet nicht.** --- Prüfen Sie, ob Sie im richtigen Kurs sind und ob ein
Textbook auswählbar ist. Wenn keine Textbooks vorhanden sind oder der WebSocket keine
Verbindung aufbauen kann, kann kein Quiz generiert werden.

**Mein Fortschritt wird nicht aktualisiert.** --- Prüfen Sie, ob Sie angemeldet sind.
Öffnen Sie eine Seite erneut oder nutzen Sie ``Mark complete``. Wenn der Server nicht
erreichbar ist, kann der Fortschritt nicht gespeichert werden.

**Ein hochgeladenes Material wird nicht verarbeitet.** --- Prüfen Sie das Dateiformat.
Unterstützt sind im Backend ``.md``, ``.markdown``, ``.html``, ``.htm``, ``.txt`` und
``.pdf``. Prüfen Sie außerdem, ob die Datei Text enthält und ob der Kurs eine Library
Group besitzt.

**Was mache ich, wenn ELISA falsche Informationen liefert?** --- Verwenden Sie die
Antwort nicht ungeprüft. Vergleichen Sie sie mit dem Skript oder fragen Sie die
Lehrperson. Sie können ELISA auch bitten, die Antwort anhand des Kursmaterials neu zu
begründen.

**An wen wende ich mich bei Problemen?** --- In einer Lehrveranstaltung wenden Sie sich
zuerst an die verantwortliche Lehrperson oder das Projektteam. Bei Login-, Rollen- oder
Systemproblemen ist die zuständige Administration die richtige Anlaufstelle.


---------------
Kurzübersicht
---------------

Die folgenden Tabellen fassen die wichtigsten Rollen und Funktionen zusammen. Sie sind
bewusst knapp gehalten und ersetzen nicht die ausführlichen Kapitel.

.. list-table:: Rollen Und Aufgaben
   :header-rows: 1
   :widths: 20 45 35

   * - Rolle
     - Aufgabe
     - Wo in ELISA?
   * - Studierende
     - Kurs öffnen, Inhalte lesen, Fragen stellen, Quiz und Spiele nutzen
     - Student Dashboard, Kurs-Chat, Skript, Quizzes, Exams, Games
   * - Lehrende
     - Kurse vorbereiten, Materialien pflegen, Skills vergeben, Studierende einschreiben
     - Teacher-Frontend, Kursliste, Kursdetailseite, Content, Students
   * - Administration
     - Benutzer, Rollen und Systemzugang verwalten
     - OpenBook-Administration und Rollenverwaltung

.. list-table:: Funktionen Und Hinweise
   :header-rows: 1
   :widths: 25 45 30

   * - Funktion
     - Zweck
     - Hinweis
   * - Kurs-Chat
     - Fragen zum ausgewählten Kurs stellen
     - Benötigt Login und WebSocket-Verbindung
   * - Skript / Content View
     - Textbook-Seiten lesen und Fortschritt speichern
     - Seiten können markiert und heruntergeladen werden
   * - Quiz
     - Verständnis mit Multiple-Choice-Fragen prüfen
     - Fragen werden kursbezogen generiert und serverseitig bewertet
   * - Exam
     - Prüfungsähnliche Übung im Kurskontext
     - PoC-Funktion, nicht als offizielle Prüfung verwenden
   * - Lernfortschritt
     - Letzte Seite, abgeschlossene Seiten und Kursabschluss speichern
     - Sichtbarkeit hängt von Login und Kursdaten ab
   * - Gamification
     - Punkte, Level, Streaks, Skills und Leaderboard anzeigen
     - Motivation, keine automatische Leistungsbewertung
   * - Memory
     - Begriffspaare aus Kursinhalten üben
     - Frontend-Spiel, nutzt Fallbacks bei fehlenden Kursdaten
   * - Flashcards
     - Kursbegriffe und Erklärungen wiederholen
     - Benötigt lesbare Kursinhalte
   * - Hangman
     - Fachbegriffe spielerisch wiederholen
     - PoC-Spiel aus Kursbegriffen
   * - Teacher Content
     - Textbooks, Seiten, Vorschau, Import und Skill-Tagging
     - Grundlage für Chat, Quiz, Spiele und Assistant-Kontext


------------------------------
Weiterführende Dokumentation
------------------------------

Die folgenden Dokumente existieren im Repository und ergänzen dieses Benutzerhandbuch.
Sie haben unterschiedliche Zielgruppen. Einige sind nutzerorientiert, andere eher für
Entwicklung, Übergabe oder Projektplanung gedacht.

.. seealso::

   * :doc:`../info_materials/students`
   * :doc:`../info_materials/teachers`
   * :doc:`../getting-started/teaching-and-learning-with-ai`
   * :doc:`../getting-started/design-decisions`
   * :doc:`../students/signup-and-account-management`
   * :doc:`../students/textbooks-and-courses`
   * :doc:`../educators/course-management`
   * :doc:`../educators/content-creation`

Die Übergabedokumentation unter ``docs/Handover/handover_next_group.txt`` beschreibt
zusätzlich den technischen Projektstand und offene Punkte für die nächste
Projektgruppe. Sie ist vor allem für Projektübergabe und Weiterentwicklung gedacht,
nicht für die alltägliche Nutzung von ELISA-AI.
