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

## Why there is no separate enrollment table

The screenshot originally suggested a separate `Course_Enrollments` table. After clarifying the requirement, the implementation uses a direct `CourseProgress -> Course` relation instead. That keeps the model smaller and avoids an extra join table that would not add behavior for the current scope.

## Files

- `src/openbook/gamification/models/course_progress.py`
- `src/openbook/gamification/admin/course_progress.py`
- `src/openbook/gamification/tests/test_course_progress.py`

## Progress

- Planned the data model and confirmed the enrollment table is not needed.
- Added the model, admin registration and initial model tests.
- Next step is to generate and verify the migration.
