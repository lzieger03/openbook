# Gamification Data Model

This document records the first implementation step for the gamification domain.

## Purpose

The new `openbook.gamification` app stores reward-related account data in a dedicated Django app instead of mixing it into `auth` or `core`.

## Initial Models

The first pass adds four persistent models:

- `Reward`: defines reward types and numeric values.
- `RewardEvent`: logs reward events for a user account and stores the event payload in `context_json`.
- `AccountPoints`: stores the current point total for one account.
- `Skill`: stores a named skill, its level, and progress for one account.

## Assumptions

- Accounts are represented by the custom OpenBook user model.
- `AccountPoints` is one-to-one with a user account.
- `Skill` entries are unique per account and skill name.
- `progress` is modeled as a percentage-like decimal in the range 0 to 100.

## Next Steps

- Add migration files for the new models.
- Wire the models into the Django admin and, if needed, DRF viewsets.
- Add fixtures if initial gamification seed data is required.
