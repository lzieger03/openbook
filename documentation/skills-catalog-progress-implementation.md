# Skills Catalog + Skill Progress Implementation

## Goal

Implement the data model from the diagram by separating:

- `Skill` as a global catalog table
- `SkillProgress` as account-specific progress rows (`Skill` 1:n `SkillProgress`)

The old account-bound `Skill` progress fields were removed and replaced by a dedicated join/progress table.

## Plan Followed

1. Refactor `Skill` model to a catalog entity (`name`, `description`, `icon_path`).
2. Introduce `SkillProgress` model with `account`, `skill`, `level`, `progress`.
3. Add API endpoints for both resources.
4. Register both resources in Django admin.
5. Add unit tests for model constraints/defaults and viewset scoping.
6. Generate migrations.
7. Wire frontend skills section to the new API-backed data shape.

## Implemented Backend Changes

### Models

- Updated: `src/openbook/gamification/models/skill.py`
- Added: `src/openbook/gamification/models/skill_progress.py`
- Updated exports: `src/openbook/gamification/models/__init__.py`

Key behavior:

- `Skill.name` is globally unique (`unique_skill_name`).
- `SkillProgress` has a unique constraint on `(account, skill)`.
- `SkillProgress.progress` is validated in range `0..100`.

### API

- Added: `src/openbook/gamification/viewsets/skill.py`
- Added: `src/openbook/gamification/viewsets/skill_progress.py`
- Updated routes: `src/openbook/gamification/routes.py`

New endpoints:

- `GET /api/gamification/skills/`
- `GET /api/gamification/skill_progress/`

Access scope:

- `Skill` endpoint is read-only catalog access.
- `SkillProgress` endpoint is read-only and scoped:
  - staff sees all rows
  - non-staff sees only own rows

### Admin

- Updated: `src/openbook/gamification/admin/skill.py`
- Added: `src/openbook/gamification/admin/skill_progress.py`
- Updated registration: `src/openbook/gamification/admin/__init__.py`

## Implemented Frontend Changes

- Updated: `src/frontend/app/src/components/sections/SkillsSection.svelte`
- Updated: `src/frontend/app/src/components/cards/SkillCard.svelte`
- Updated integration: `src/frontend/app/src/components/pages/gamification/GamificationManualTestPage.svelte`

Behavior now:

- Manual gamification test page loads `skill_progress` with `_expand=skill`.
- Skill cards render using catalog fields (`name`, `description`, `icon_path`) plus per-account progress (`level`, `progress`).

## Migrations

- Added: `src/openbook/gamification/migrations/0010_skillprogress_alter_skill_options_and_more.py`

Migration includes:

- `CreateModel(SkillProgress)`
- remove old `Skill` account/progress fields
- add new `Skill` catalog fields and unique constraint

## Validation Results

### Django tests

Command:

```bash
poetry run python src/manage.py test openbook.gamification.tests.test_skill openbook.gamification.tests.test_skill_progress
```

Result: passed.

Command:

```bash
poetry run python src/manage.py test openbook.gamification.tests
```

Result: passed.

### Frontend build

Command:

```bash
cd src/frontend/app
npm run build
```

Result: successful build (`EXIT:0`) and generated API client files for `Skill` and `SkillProgress`.

## Notes

- Decision was "schema clean": old `Skill` data is not migrated into `SkillProgress`.
- The generated API client now includes new skill-related files in `src/frontend/app/src/api-client/`.
