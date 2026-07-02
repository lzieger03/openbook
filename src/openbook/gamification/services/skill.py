# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

"""
Advance a learner's progress in a single global skill.

A skill is tracked per account as a level plus a 0–100 % progress bar
(``SkillProgress``). Earning skill progress raises that bar; whenever it reaches
100 % the skill levels up and the overflow carries over into the next level. This
is how doing skill-related work in a course (e.g. answering an HTML quiz question)
makes the matching skill grow on the learner's dashboard.
"""

from decimal import Decimal

from django.db import transaction

from ..models.skill_progress import SkillProgress


def get_skill_progress_state(account_id, skill_id) -> dict:
    """
    Return the current progress for an account in one skill. Skills the account has
    not trained yet are reported as a fresh level-1 skill at 0 %.
    """
    progress = SkillProgress.objects.filter(account_id=account_id, skill_id=skill_id).first()

    if progress is None:
        return {
            "skill_level":    1,
            "skill_progress": Decimal("0"),
        }

    return {
        "skill_level":    progress.level,
        "skill_progress": progress.progress,
    }


@transaction.atomic
def award_skill_progress(account_id, skill_id, amount) -> dict:
    """
    Add ``amount`` percentage points of progress to ``skill_id`` for ``account_id``.

    Each time the progress bar fills past 100 % the skill levels up and the overflow
    carries into the next level (so a large award can grant several levels at once).
    ``amount`` must be a positive number. Returns the updated skill progress state.
    """
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValueError("Cannot award a non-positive amount of skill progress.")

    # Make sure a progress row exists, then apply the delta atomically. select_for_update
    # keeps concurrent awards for the same account/skill from clobbering each other.
    progress, _ = SkillProgress.objects.get_or_create(account_id=account_id, skill_id=skill_id)
    progress = SkillProgress.objects.select_for_update().get(pk=progress.pk)

    total     = progress.progress + amount
    level_ups = int(total // 100)
    remainder = total - level_ups * 100

    if level_ups:
        progress.level += level_ups

    progress.progress = remainder
    progress.save(update_fields=["level", "progress"])

    return get_skill_progress_state(account_id, skill_id)
