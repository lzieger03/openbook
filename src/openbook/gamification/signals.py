# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.contrib.auth      import get_user_model
from django.db.models         import F
from django.db.models.signals import post_save
from django.dispatch          import receiver

from .models import AccountPoints, RewardEvent

User = get_user_model()


@receiver(post_save, sender=User)
def create_account_points(sender, instance, created, **kwargs):
    """
    Automatically create an AccountPoints entry when a new user is created.
    """
    if created:
        AccountPoints.objects.get_or_create(
            account=instance,
            defaults={"point_total": 0}
        )


@receiver(post_save, sender=RewardEvent)
def update_account_points_on_reward_event(sender, instance, created, **kwargs):
    """
    Automatically update AccountPoints.point_total when a RewardEvent is created.
    """
    if created:
        account_points, _ = AccountPoints.objects.get_or_create(
            account=instance.account,
            defaults={"point_total": 0}
        )

        AccountPoints.objects.filter(pk=account_points.pk).update(
            point_total=F("point_total") + instance.points_delta,
        )
