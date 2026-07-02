================================
Information For Teachers
================================

ELISA is a proof of concept for supporting teaching and self-study in OpenBook. This page explains
how teachers can understand its value, where it can fit into a course, and what should be handled
carefully.

.. contents:: Page Content
   :local:


-------------------
Teaching Value
-------------------

ELISA is meant to support students while they work through course material. It combines content,
course-aware chat, quiz interactions, progress data, and early gamification concepts. For teachers,
the main value is that students can practice more independently while the system records learning
signals that may later support feedback.

The student branches include a teacher frontend with course list and course detail views. The
documented direction is a simpler interface for course content and student-related course work. This
is separate from the general Django admin and is intended to be more approachable for teaching use.


-------------------
Typical Use Cases
-------------------

Teachers can use ELISA as part of a self-study course. Students read content in the dashboard, ask
questions through the course chat, and use quiz interactions to check their understanding. This can
make independent learning more structured.

The learning state and quiz result concepts create a basis for progress views. In a later stable
version, these data can help teachers see which content students worked on and where they struggled.
In the current proof of concept, this should be treated as a technical foundation rather than a full
analytics product.

Gamification can make activity visible through points, skills, rewards, streaks, and course
progress. It should be used carefully. The goal is to support regular practice and orientation, not
to turn learning into a point hunt.


---------------------------
Responsible AI Use
---------------------------

Teachers should define clear rules for AI use in their courses. Students need to know when they may
use the assistant, whether AI support is allowed for assignments, and how they should verify AI
answers.

The assistant should not be treated as an authoritative teacher replacement. It can explain,
summarize, ask practice questions, and help students revisit content. Teachers remain responsible
for course design, assessment, feedback, and deciding which answers or quiz questions are valid.

Before using AI-generated questions or explanations in formal teaching material, review them. The
proof of concept can generate helpful practice content, but it does not guarantee correctness,
completeness, or didactic quality.


-------------------
Current Limits
-------------------

ELISA is not yet a finished teaching platform. Some teacher-facing screens and backend services are
present in student branches, but the final workflow still needs stabilization. Reporting and
assessment workflows are not documented as complete.

Open points include final reward rules, explicit course completion handling, quiz point assignment,
and long-term memory entries for learning behavior. Local setup problems can also affect API schema
generation and documentation builds when the database is not initialized.
