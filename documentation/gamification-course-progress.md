# Gamification Course Progress

This change adds a new gamification table for per-course progress tracking.

## Data Model

The new `CourseProgress` model stores:

- the user account
- the course
- the current course points
- the current course level
- the current course progress percentage

The model uses a unique constraint on `(account, course)` so each user can only have one progress row per course.

## API and UI

The model is exposed through a read-only gamification API endpoint at `/api/gamification/course_progress/`. The frontend gamification test page uses that endpoint to show the selected user's course progress as a list of cards with level, points and a visual progress bar.

## Why there is no separate enrollment table

The screenshot originally suggested a separate `Course_Enrollments` table. After clarifying the requirement, the implementation uses a direct `CourseProgress -> Course` relation instead. That keeps the model smaller and avoids an extra join table that would not add behavior for the current scope.

## Files

- `src/openbook/gamification/models/course_progress.py`
- `src/openbook/gamification/admin/course_progress.py`
- `src/openbook/gamification/tests/test_course_progress.py`
- `src/openbook/gamification/viewsets/course_progress.py`
- `src/frontend/app/src/components/pages/gamification/GamificationManualTestPage.svelte`

## Progress

- Planned the data model and confirmed the enrollment table is not needed.
- Added the model, admin registration and initial model tests.
- Added the API endpoint and wired the gamification test page to show course progress.
- Next step is to run frontend checks and confirm the generated API/client state stays clean.
