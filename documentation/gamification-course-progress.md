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

## Earning points inside a course

Course progress is advanced through the `award_course_points` service in
`src/openbook/gamification/services/course.py`. Calling

```python
from openbook.gamification.services import award_course_points

award_course_points(account_id, course_id, points)
```

does two things in one transaction:

1. **Per-course progress.** It creates the `CourseProgress` row if needed and adds
   the points. The course level is recomputed from the shared `LevelThreshold`
   table and `course_progress` (the 0–100 % bar shown on each course card) is set to
   the progress from the current level threshold towards the next one. The bar fills
   up with every point and resets on each course level-up.

2. **Global progress.** The same point delta is written to the `RewardEventLog` as a
   `COURSE_POINTS_AWARDED` event. The existing reward-event signal then raises the
   account's overall `point_total`, recomputes the global level and advances the
   daily streak. This is how points earned inside a course also move the overall
   level and point system.

`LevelThreshold.progress_to_next_level(points)` centralises the "progress bar"
calculation so the account dashboard and the per-course bar share the same logic.

### Awarding points from the UI

The service is also exposed as a write action at
`POST /api/gamification/course_progress/award/` with a body of
`{"course": "<uuid>", "points": <int>, "account"?: "<username>", "context"?: {}}`.
Non-staff users may only award points to themselves. The gamification manual test
page (section 5) uses this endpoint: pick a course and a point amount (or use the
per-card +5/+10/+25 buttons) and watch the course progress bar, the global point
total/level (section 3) and the reward event log (section 6) update live.

## Why there is no separate enrollment table

The screenshot originally suggested a separate `Course_Enrollments` table. After clarifying the requirement, the implementation uses a direct `CourseProgress -> Course` relation instead. That keeps the model smaller and avoids an extra join table that would not add behavior for the current scope.

## Files

- `src/openbook/gamification/models/course_progress.py`
- `src/openbook/gamification/models/level_threshold.py` (`progress_to_next_level`)
- `src/openbook/gamification/services/course.py` (`award_course_points`)
- `src/openbook/gamification/constants.py` (`CourseEventType`)
- `src/openbook/gamification/admin/course_progress.py`
- `src/openbook/gamification/tests/test_course_progress.py`
- `src/openbook/gamification/viewsets/course_progress.py`
- `src/frontend/app/src/components/pages/gamification/GamificationManualTestPage.svelte`

## Progress

- Planned the data model and confirmed the enrollment table is not needed.
- Added the model, admin registration and initial model tests.
- Added the API endpoint and wired the gamification test page to show course progress.
- Added the `award_course_points` service plus the `/award/` write endpoint so points earned in a course also raise the global level and point total.
- Next step is to run frontend checks and confirm the generated API/client state stays clean.
