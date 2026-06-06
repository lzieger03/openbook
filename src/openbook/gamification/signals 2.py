# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django.contrib.auth      import get_user_model
from django.db.models         import F
from django.db.models.signals import post_save
from django.dispatch          import receiver

from .constants               import StreakEventType
from .models                  import AccountProgress, LevelThreshold, RewardEventLog
from .services.streak         import update_streak_for_points

User = get_user_model()


@receiver(post_save, sender=User)
def create_account_progress(sender, instance, created, **kwargs):
    """
    Automatically create an AccountProgress entry when a new user is created.
    Accounts start at level 1.
    """
    if created:
        AccountProgress.objects.get_or_create(
            account=instance,
            defaults={"point_total": 0, "level": 1}
        )


@receiver(post_save, sender=RewardEventLog)
def update_account_progress_on_reward_event(sender, instance, created, **kwargs):
    """
    Automatically update AccountProgress.point_total when a RewardEventLog entry is
    created, recompute the level from the configured LevelThreshold table and
    advance the daily streak whenever the account actually earns points.
    """
    if not created:
        return

    account_progress, _ = AccountProgress.objects.get_or_create(
        account=instance.account,
        defaults={"point_total": 0, "level": 1}
    )

    AccountProgress.objects.filter(pk=account_progress.pk).update(
        point_total=F("point_total") + instance.points_delta,
    )

    account_progress.refresh_from_db()

    new_level = LevelThreshold.level_for_points(account_progress.point_total)

    if new_level != account_progress.level:
        AccountProgress.objects.filter(pk=account_progress.pk).update(level=new_level)

    # Recompute the streak only for genuine point-earning events. Streak bookkeeping
    # entries carry a zero delta, so this also prevents the signal from recursing.
    if instance.points_delta != 0 and instance.event_type not in StreakEventType.values:
        update_streak_for_points(instance.account_id, instance.created_at)
