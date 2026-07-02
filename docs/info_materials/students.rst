================================
Information For Students
================================

ELISA is a proof of concept for AI-supported learning in OpenBook. This page explains what students
can use ELISA for, what benefits it can provide, and where its current limits are.

.. contents:: Page Content
   :local:


------------------
What ELISA Offers
------------------

ELISA is designed as a learning companion for course-based self-study. It connects course content,
chat, quiz questions, progress tracking, and first gamification elements. The goal is to help you
work more actively with learning material instead of only reading pages passively.

In the current proof of concept, ELISA focuses on a student dashboard, course content, a course-aware
chat, quiz interactions, and visible learning progress. Some parts are already represented in code
and documented frontend screens. Other parts are still experimental and may change in the next
project phase.


-------------------
Typical Use Cases
-------------------

You can use ELISA while working through a course. Open the course content, read the current page, and
use the chat when a concept is unclear. The assistant should answer in the context of the selected
course and can use course documents where they are available.

You can also use quiz interactions to check your understanding. The documented quiz flow generates
multiple-choice questions through the course assistant. Quiz results can be stored so weak areas may
become visible later.

Progress and gamification elements help you see activity. They can show what you have worked on,
which skills or rewards are connected to learning activity, and whether you are building a regular
learning rhythm. These signals should motivate practice, not replace real understanding.


---------------------------
Responsible AI Use
---------------------------

Use ELISA to learn, not to avoid learning. Ask the assistant to explain concepts, compare examples,
or help you identify what you have not understood yet. A useful question is specific, names the
course topic, and explains what is confusing.

AI-generated answers can be wrong or incomplete. Check important answers against the course content
and your teacher's instructions. If an answer sounds uncertain or conflicts with the material, treat
it as a reason to ask follow-up questions or contact your teacher.

Do not treat generated quiz questions as official exam preparation unless your teacher explicitly
says so. They are useful for practice, but they need validation before they can be considered
reliable assessment material.


-------------------
Current Limits
-------------------

ELISA is currently a proof of concept. Some flows are implemented, some are integrated through
student branches, and some are documented as open work. The system may not behave consistently in
every local setup.

Important limitations are that reward rules are not final, course completion handling is still open,
and AI responses need human validation. The project also depends on a correctly prepared local
OpenBook installation. If the database is not migrated, some generated documentation and API-related
steps can fail.
