from __future__ import annotations

import logging

from django.db.models.signals import post_save
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


# NOTE: Kursabschluss (COURSE_COMPLETION) wird bewusst NICHT mehr automatisch aus
# completed_pages abgeleitet. Der Abschluss ist eine explizite Aktion (Button am
# Kursende -> Orchestrator -> DB). Der konkrete Endpoint/Vertrag wird noch mit dem
# Orchestrator-Team geklärt. Siehe README "Noch offen".
