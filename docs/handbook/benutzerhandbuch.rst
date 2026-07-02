=====================
ELISA User Handbook
=====================

ELISA is the student project name for the OpenBook learning assistant proof of concept. This
handbook explains the current user-facing idea of ELISA for students, teachers, and general users.
It is based on the repository state, the student branches, and the documentation notes available in
this project.

.. contents:: Page Content
   :local:


----------------
What ELISA Is
----------------

ELISA combines OpenBook's interactive textbook concept with learning support features developed in
student branches. The proof of concept focuses on courses, course content, an AI-supported chat,
quiz interactions, learning progress, and first gamification elements. The goal is not to replace
teachers. ELISA should help learners work through content more actively and give teachers a better
starting point for supporting self-study.

OpenBook already provides the larger platform context: accounts, courses, textbooks, pages, and
administration. The ELISA work adds user-facing learning support around that structure. From a user
perspective, the system is meant to answer questions about course material, generate quiz-like
interactions, remember basic progress signals, and make learning activity more visible.

The current state is a proof of concept. Some features are implemented as backend models, APIs, or
frontend screens, while other parts are documented as intended flows or integration points. This
handbook therefore describes the intended usage and clearly marks current limitations.


------------------
Available Features
------------------

The student branches add several feature areas that together form the ELISA learning experience. The
most important areas are the student dashboard, teacher area, assistant and RAG integration, quiz
flow, learning state, and gamification.

**Learning content** -- Courses contain textbook pages and related learning material. Students work
through these pages in the dashboard and can use the content view as their main reading interface.
The teacher area contains screens for listing courses, opening course details, and managing course
content in a simplified interface.

**AI chat** -- The assistant is designed as a course-aware chat. It uses the current course context
and, where available, uploaded or synchronized course documents. The repository contains an
assistant app with services for chat handling, prompt building, RAG access, vector indexing, and
learning context. The frontend documentation describes a course chat page and a chat widget.

**Quiz flow** -- Quiz interactions are connected to the course assistant flow. The documented
behavior says that the frontend sends a quiz start event through the course chat WebSocket. The
assistant then generates multiple-choice questions from RAG documents or from course context such as
course data, skills, and textbook pages. Later student work also adds server-side quiz grading.

**Learning progress** -- The learning app records a learner's course state and quiz results. The
`LearningState` concept stores the course, last page, completed pages, and last access time. The
`QuizResult` concept stores quiz scores and attempts per user and page. These data points can be
used by the assistant to tailor context and by the UI to show progress.

**Gamification** -- The gamification work introduces points, rewards, skills, streaks, course
progress, and event logs. From a user perspective this can make learning activity visible through
progress cards, skill cards, rewards, streak state, and course progress. Some pieces are backend
focused, while dashboard components and documented UI sections show how these values are intended to
appear in the student interface.


------------------------
Using ELISA As A Student
------------------------

Students use ELISA as a guided self-study environment. The typical entry point is the student
dashboard. It is intended to show enrolled courses, learning progress, skills, statistics, and
access to course content, quizzes, and chat.

A typical student workflow starts by opening the dashboard and selecting a course. The student reads
the available content page by page. When a page or chapter is completed, the learning state can be
updated so the system knows the last visited page and completed pages. This information is useful
for progress views and for the assistant's course context.

When a student has a question, the course chat can be used to ask about the course material. The
assistant should answer within the context of the selected course. If RAG documents are available,
the assistant can use those documents as additional context. If no RAG documents are available, the
documented fallback is to use course data, skills, and textbook pages.

Students can also start a quiz flow. In the documented design, quiz questions are generated through
the course-aware assistant flow and returned as multiple-choice questions. Quiz results are meant to
be stored so weak areas can become visible later. This enables a learning loop: read content, ask
questions, test understanding, and continue with feedback.

Gamification elements support motivation. Points, skills, rewards, streaks, and course progress are
not the learning goal by themselves. They make activity visible and can help learners understand
what they have already done. In the proof of concept, the exact reward rules are still partly open
and should be treated as experimental.


------------------------
Using ELISA As A Teacher
------------------------

Teachers use ELISA to prepare course structures and support student self-study. The student branches
contain a dedicated teacher frontend with a course list, course detail page, content panel, overview
panel, and student panel. The goal is to provide a focused interface for course-related work without
requiring teachers to use low-level administration pages for every task.

A typical teacher workflow starts with opening the teacher area and selecting a course. The course
detail view is intended to show overview information, enrolled students, and course content. The
content panel focuses on adding or managing learning material with a simpler user experience than a
pure admin backend.

Teachers benefit from ELISA when students use the dashboard, chat, quiz, and progress features
regularly. Learning state and quiz results can reveal where students are active and where they have
difficulty. In the proof of concept, these data are primarily technical building blocks and frontend
views. A final pedagogical reporting workflow is still open.

The AI assistant should be used as a support channel, not as an authoritative replacement for
teaching. Teachers should still define learning goals, validate content quality, and explain how
students should use AI responsibly. ELISA can support preparation and practice, but course design
and assessment responsibility remain with the teacher.


---------------------------------
Learning Content, Chat, And Quiz
---------------------------------

ELISA connects learning content, chat, and quiz flows around the selected course. The course is the
main context boundary. This matters because a question or quiz should relate to the current course,
not to unrelated material.

The assistant implementation in the student branches introduces RAG document storage and services.
RAG means that course documents can be indexed and used as retrieval context for assistant answers.
The branch documentation also describes synchronizing course textbooks into assistant documents, so
course content can become part of the assistant context.

Quiz generation is documented as a WebSocket interaction. The frontend sends a quiz start event to
the course chat channel. The backend generates questions and sends a quiz generated event back. A
later branch adds server-side grading, which means scoring is not only a frontend concern.

For users, the important point is simple: ELISA should keep learning interactions near the course
content. Students read a page, ask questions about it, take a quiz, and continue learning. Teachers
prepare the course context and review whether the interaction supports their intended learning
process.


-------------------------------------
Learning Progress And Gamification
-------------------------------------

Learning progress is represented through stored learning state and quiz results. The learning state
tracks the course, the last visited page, completed pages, and access time. Quiz results track the
page, score, attempts, and answer time. These data points are meant to help ELISA understand where a
student currently stands.

Gamification adds a second layer of feedback. It can record activity events, update streaks, assign
points, maintain skill progress, and show rewards. The student documentation notes that viewing or
completing content can update the streak without necessarily awarding points. Course completion and
quiz point rules are still open in the documented learning notes.

Users should treat gamification as orientation and motivation. A high point value does not prove deep
understanding, and a low value does not mean failure. The feature is useful when it encourages
regular practice and makes progress visible, but it should not replace teacher feedback or formal
assessment.


-----------------------------------
Responsible Use Of AI In ELISA
-----------------------------------

ELISA's assistant can help learners ask better questions, revisit explanations, and practice with
quiz questions. Students should use it to understand course content, not to bypass their own work.
Good prompts include the course topic, the page or concept, and what is unclear.

Teachers should explain when AI support is allowed and how it may be used in assignments. They
should also remind students that AI answers can be incomplete or wrong. Course material, teacher
instructions, and verified references remain the authoritative sources.

The proof of concept should not be used for high-stakes assessment without further validation. Quiz
questions and assistant answers need review before they can be treated as reliable examination
material. Stored progress and gamification data should also be interpreted carefully.


--------------------------------
Proof Of Concept Limitations
--------------------------------

The current ELISA state is not a finished product. The repository contains several integrated
student branches and some features are documented as intended or partly implemented. The handover
document lists the exact branches and components that were analyzed.

Known limitations include the following:

* The full documentation build can fail when the local Django database is not migrated, because the
  OpenAPI sync endpoint needs tables such as `django_site`.
* Some generated OpenAPI files may be missing when the OpenAPI sync does not complete.
* The exact rules for quiz points and course completion rewards are still open in the learning
  documentation.
* The memory-entry idea for storing longer-term learning behavior is documented as not built.
* Some frontend build outputs and generated files appear in integration branches and should be
  cleaned up before production use.
* Teacher-facing reporting is present as a direction, but not documented as a complete final
  workflow.
* AI answers and generated quizzes require validation and should not be treated as authoritative.

These limitations do not make the proof of concept unusable. They define the boundary for the next
project group: stabilize the integration, decide the final learning and reward rules, improve the
teacher workflow, and validate the AI-supported learning loop.
