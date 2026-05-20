# Gamification System

This document records the implementation progress for the gamification domain in OpenBook.

## Purpose

The new `openbook.gamification` app provides a dedicated backend for reward-related account data, including point tracking, reward definitions, event audit logs, and skill progression.

## Data Model

### Core Models

The gamification system consists of four persistent models:

1. **Reward**
   - Defines reward types and their integer point values.
   - Fields: `reward_type` (string), `value` (integer points), `description` (optional text)
   - Use case: Admin defines "Question Correct" = 10 points, "Quiz Complete" = 50 points, etc.

2. **AccountPoints**
   - One-to-one relationship with user accounts.
   - Stores the current total points for a user.
   - Fields: `account` (OneToOne to User), `point_total` (integer, default 0), `updated_at` (auto-updated timestamp)
   - Use case: User has accumulated 250 points total.
   - **Auto-created** when a new user is registered (via Django signal).

3. **RewardEvent**
   - Audit log of all point transactions.
   - Records what reward was granted, to which user, when, and optional context.
   - Fields: `account` (FK to User), `reward` (FK to Reward), `event_type` (string), `points_delta` (integer), `created_at` (timestamp), `context` (JSON)
   - Use case: "User lars completed Quiz #5" → RewardEvent created with points_delta=50.
   - **Automatically updates** user's `AccountPoints.point_total` when created (via Django signal).

4. **Skill**
   - Tracks named skills per user, including level and progress.
   - Fields: `account` (FK to User), `name` (string, unique per account), `level` (integer), `progress` (decimal 0–100)
   - Use case: Tracking "Python Programming" level 2, 75% progress.

## Automatic Behaviors

### Signal: User Registration → AccountPoints
When a new user is created, a signal handler in `signals.py` automatically creates an `AccountPoints` entry with `point_total=0`.

```python
@receiver(post_save, sender=User)
def create_account_points(sender, instance, created, **kwargs):
    if created:
        AccountPoints.objects.get_or_create(
            account=instance,
            defaults={"point_total": 0}
        )
```

### Signal: RewardEvent Creation → Point Update
When a `RewardEvent` is created, a signal handler automatically updates the user's `AccountPoints.point_total` by adding `points_delta`.

```python
@receiver(post_save, sender=RewardEvent)
def update_account_points_on_reward_event(sender, instance, created, **kwargs):
    if created:
        account_points = AccountPoints.objects.get(account=instance.account)
        account_points.point_total += instance.points_delta
        account_points.save()
```

**Key Workflow:**
1. Admin (or API) creates a `RewardEvent` for a user with `points_delta=50`.
2. Signal fires → user's `AccountPoints.point_total` is incremented by 50.
3. `RewardEvent` remains in database as immutable audit log.

## Backend Implementation

### Django App: `openbook.gamification`

**Location:** `src/openbook/gamification/`

**Structure:**
- `models/`: Four model files (`reward.py`, `account_points.py`, `reward_event.py`, `skill.py`)
- `admin/`: Django admin classes with optimizations (raw_id_fields, list_select_related, list_editable)
- `migrations/`: Auto-generated migration files (0001_initial.py, 0002_alter_reward_value.py)
- `signals.py`: Signal handlers for automatic AccountPoints creation and point updates
- `apps.py`: AppConfig with signal registration in `ready()` method
- `routes.py`: Placeholder for DRF viewsets (not yet implemented)
- `__init__.py`: Model imports

### Admin Interface

All four models are registered with customized admin classes in `src/openbook/gamification/admin/__init__.py`:

- **RewardAdmin**
  - `list_display`: reward_type, value, description
  - `list_editable`: value (edit points directly in list view)
  - `ordering`: reward_type, -value

- **AccountPointsAdmin**
  - `list_display`: account, point_total, updated_at
  - `raw_id_fields`: account (fast user lookup)
  - `list_select_related`: account (single query optimization)
  - `readonly_fields`: updated_at (automatically set)

- **RewardEventAdmin**
  - `list_display`: account, reward, event_type, points_delta, created_at
  - `raw_id_fields`: account, reward (fast lookups)
  - `list_select_related`: account, reward (optimize queries)
  - `readonly_fields`: created_at, context (immutable audit log)

- **SkillAdmin**
  - `list_display`: account, name, level, progress
  - `list_filter`: level (filter by skill level)
  - `search_fields`: account.username, account.email, name
  - `raw_id_fields`: account (fast lookup)
  - `list_select_related`: account (optimize queries)

**URL:** http://localhost:8000/admin/ → OpenBook section → Gamification models

### Database Schema

Migrations applied:
- `0001_initial.py`: Create all four models
- `0002_alter_reward_value.py`: Change Reward.value from DecimalField to IntegerField

## Frontend Implementation

### Svelte Dashboard: `/app/#/gamification`

**Location:** `src/frontend/app/src/components/pages/gamification/GamificationPage.svelte`

**Components:**
- `AccountPointsCard.svelte`: Displays current user point total
- `SkillsSection.svelte` + `SkillCard.svelte`: Shows user skills with level and progress
- `RewardsSection.svelte` + `RewardCard.svelte`: Lists available rewards
- `RewardEventsSection.svelte`: Shows recent reward events (transactions)

**Current Status:**
- Uses mock data (hardcoded examples)
- Route registered in `src/frontend/app/src/components/routes.ts`
- SPA served under `/app/` with fallback routing (SPA index on `/app/#/*`)

**Next Steps:**
- Replace mock data with API calls (once DRF endpoints are implemented)
- Add authentication/user context
- Implement error handling and loading states

## Workflow: Creating and Granting Rewards

### Step 1: Define a Reward (Admin)
1. Go to http://localhost:8000/admin/
2. OpenBook → Gamification → Rewards
3. Click "Add Reward"
4. Fill in: Reward Type (e.g., "Question Correct"), Value (e.g., 10 points), Description
5. Save

### Step 2: Grant a Reward to a User (Admin)
1. Go to http://localhost:8000/admin/
2. OpenBook → Gamification → Reward events
3. Click "Add Reward event"
4. Select Account (user), Reward (from Step 1), Event Type (optional), Points Delta (auto-filled or override)
5. Save

**What happens automatically:**
- Signal fire → User's `AccountPoints.point_total` incremented
- `RewardEvent` stored as immutable audit log

### Step 3: View Points (Frontend)
- Navigate to http://localhost:8000/app/#/gamification
- See updated point total, skills, and reward history

## TODO / Next Steps

- [ ] Implement DRF serializers and viewsets in `routes.py`
- [ ] Connect frontend dashboard to real API endpoints
- [ ] Add admin actions (e.g., "Grant 100 points to selected users", "Revoke reward")
- [ ] Add admin inlines (e.g., show RewardEvents inline on AccountPoints detail)
- [ ] Add unit tests for models, signals, and admin
- [ ] Create fixtures for initial gamification data (if needed)
- [ ] Add API documentation (drf-spectacular integration)
- [ ] Handle legacy users without AccountPoints (batch creation management command)
