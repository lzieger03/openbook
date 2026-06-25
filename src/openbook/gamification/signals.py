# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.contrib.auth      import get_user_model
from django.db.models         import F
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch          import receiver

from openbook.auth.models     import Role, RoleAssignment
from openbook.content.models.course import Course

from .constants               import StreakEventType
from .models                  import AccountProgress, CourseProgress, LevelThreshold, RewardEventLog
from .services.streak         import update_streak_for_points

User = get_user_model()

# Slug of the per-course role that marks a user as an enrolled student. Mirrors
# STUDENT_ROLE_SLUG in the teacher frontend (src/frontend/teacher/src/api/enrollment.ts).
STUDENT_ROLE_SLUG = "student"


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


def _is_student_course_enrollment(instance) -> bool:
    """
    Return whether the given role assignment enrolls a user as a student into a course.

    Enrollment is modeled as a "student" role assignment in the course scope. The role
    is looked up defensively (rather than via ``instance.role``) so this also works from
    ``post_delete``, where the related role may already have been cascade-deleted.
    """
    if instance.scope_type_id is None or instance.role_id is None:
        return False

    if instance.scope_type.model_class() is not Course:
        return False

    role = Role.objects.filter(pk=instance.role_id).first()
    return role is not None and role.slug == STUDENT_ROLE_SLUG


@receiver(post_save, sender=RoleAssignment)
def create_course_progress_on_enrollment(sender, instance, created, **kwargs):
    """
    Ensure a CourseProgress row exists when a student is enrolled into a course.

    The dashboard lists a learner's courses from their CourseProgress rows, so without
    this a freshly enrolled student would not see the course until they earned their
    first points. Creating a zeroed progress row makes the course show up immediately.
    """
    if not _is_student_course_enrollment(instance):
        return

    if not Course.objects.filter(pk=instance.scope_uuid).exists():
        return

    CourseProgress.objects.get_or_create(
        account_id=instance.user_id,
        course_id=instance.scope_uuid,
    )


@receiver(post_delete, sender=RoleAssignment)
def remove_course_progress_on_unenrollment(sender, instance, **kwargs):
    """
    Drop the placeholder CourseProgress row when a student is unenrolled, but only when
    they have not earned any points yet. This removes the empty rows created on
    enrollment while preserving the real progress and history of learners who advanced.
    """
    if not _is_student_course_enrollment(instance):
        return

    CourseProgress.objects.filter(
        account_id=instance.user_id,
        course_id=instance.scope_uuid,
        course_points=0,
    ).delete()
