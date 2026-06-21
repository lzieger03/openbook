from __future__ import annotations

import logging

from django.db.models.signals import m2m_changed, post_save
from django.dispatch          import receiver

from .models.state import LearningState

logger = logging.getLogger(__name__)


@receiver(post_save, sender=LearningState)
def record_content_viewed(sender, instance, **kwargs):
    """Advance the daily learning streak when a user accesses content."""
    try:
        from openbook.gamification.constants      import LearningActivityType
        from openbook.gamification.services.streak import record_learning_activity

        record_learning_activity(instance.user_id, LearningActivityType.CONTENT_VIEWED)
    except Exception:
        logger.exception("Gamification streak update failed for user %s", instance.user_id)


@receiver(m2m_changed, sender=LearningState.completed_pages.through)
def check_course_completion(sender, instance, action, **kwargs):
    """Award COURSE_COMPLETION points when all pages of a course are done."""
    if action != "post_add":
        return

    try:
        from openbook.content.models              import TextbookPage
        from openbook.gamification.models         import Reward, RewardEventLog

        course_page_ids = set(
            TextbookPage.objects
            .filter(textbook__used_in_courses__course=instance.course)
            .values_list("id", flat=True)
        )

        if not course_page_ids:
            return

        completed_ids = set(instance.completed_pages.values_list("id", flat=True))

        if not course_page_ids.issubset(completed_ids):
            return

        already_awarded = RewardEventLog.objects.filter(
            account=instance.user,
            event_type="COURSE_COMPLETION",
            context__course_id=str(instance.course_id),
        ).exists()

        if already_awarded:
            return

        reward = Reward.objects.filter(reward_type="COURSE_COMPLETION").first()
        if not reward:
            logger.warning("No COURSE_COMPLETION reward defined in database")
            return

        RewardEventLog.objects.create(
            account      = instance.user,
            reward       = reward,
            event_type   = "COURSE_COMPLETION",
            points_delta = int(reward.value),
            context      = {"course_id": str(instance.course_id)},
        )
    except Exception:
        logger.exception(
            "Gamification course completion check failed for user %s, course %s",
            instance.user_id,
            instance.course_id,
        )
