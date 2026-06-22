# Gamification API Route Registration Fix

## Purpose
Resolve gamification API integration issues by wiring the existing DRF viewsets into the global API router and ensuring reward-event signals are loaded.

## Plan
1. Inspect URL registration chain from `openbook.urls` to gamification route registration.
2. Register all existing gamification viewsets in `src/openbook/gamification/routes.py`.
3. Validate that `/api/gamification/rewards/` is reachable.
4. Restore signal registration so reward events update account point totals.
5. Record outcome and known follow-up risks.

## Progress
- Completed: Located root cause in `src/openbook/gamification/routes.py`; route registration was a stub returning `None`.
- Completed: Added router registrations for:
  - `gamification/rewards` (basename: `reward`)
  - `gamification/account_points` (basename: `account_points`)
  - `gamification/reward_events` (basename: `reward_event`)
- Completed: Validation test passed:
  - `python manage.py test openbook.gamification.tests.test_reward.Reward_ViewSet_Tests.test_list_authorized`
- Completed: Restored `GamificationApp.ready()` to import `openbook.gamification.signals`.
- Completed: Validation tests passed:
  - `python manage.py test openbook.gamification.tests.test_signals openbook.gamification.tests.test_reward_event.RewardEvent_ViewSet_Tests.test_trigger_creates_reward_event_and_updates_points openbook.gamification.tests.test_reward_event.RewardEvent_ViewSet_Tests.test_staff_can_trigger_for_other_account`
- Completed: Manual browser verification passed; triggering `level_completed` changed the point total from 30 to 130.
- Observation: Running the full gamification test subset now leaves one unrelated failure in `Reward_ViewSet_Tests.test_list_sort`, where the generic test helper compares serialized decimal strings lexicographically.

## Result
The endpoint `/api/gamification/rewards/` is now registered and reachable through Django REST Framework routing. New reward events now increment the matching `AccountPoints.point_total` through the restored signal registration.
