"""Create idempotent dummy gamification data for local development.

Creates three demo users, a small set of `Skill` entries and corresponding
`SkillProgress` records. Supports `--clear` to remove the demo data first.

This command is intentionally safe and idempotent: re-running will not create
duplicate objects.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable
import datetime

from django.utils import timezone

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from openbook.gamification.models import (
    Skill,
    SkillProgress,
    AccountProgress,
    AccountActivityDay,
    AccountStreak,
    Reward,
    RewardEventLog,
    LevelThreshold,
    CourseProgress,
)
from openbook.content.models import Course


DEMO_USERS = [
    {"username": "max.mustermann", "email": "max@example.com", "first_name": "Max", "last_name": "Mustermann"},
    {"username": "jane.doe", "email": "jane@example.com", "first_name": "Jane", "last_name": "Doe"},
    {"username": "demo.user", "email": "demo@example.com", "first_name": "Demo", "last_name": "User"},
]

DEMO_SKILLS = [
    {"name": "Collaboration", "description": "Work well with others.", "icon_path": "icons/collaboration.svg"},
    {"name": "Problem Solving", "description": "Solve course problems.", "icon_path": "icons/problem-solving.svg"},
    {"name": "Persistence", "description": "Keep trying until solved.", "icon_path": "icons/persistence.svg"},
]


class Command(BaseCommand):
    help = "Load idempotent dummy gamification data for local development."

    def add_arguments(self, parser) -> None:  # noqa: D401 - simple CLI
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete demo users, skills and skill progress before creating them.",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        clear = options.get("clear", False)

        with transaction.atomic():
            if clear:
                self.stdout.write("Clearing demo data...")
                self._clear_demo_data(User)

            created_users = self._ensure_users(User)
            created_skills = self._ensure_skills()
            created_progress = self._ensure_skill_progress(created_users, created_skills)
            created_levels = self._ensure_level_thresholds()
            created_rewards = self._ensure_rewards()
            created_account_progress = self._ensure_account_progress(created_users)
            created_activity_days = self._ensure_activity_days(created_users)
            created_streaks = self._ensure_account_streaks(created_users)
            created_events = self._ensure_reward_event_logs(created_users, created_rewards)
            created_course_progress = self._ensure_course_progress(created_users)

        self.stdout.write(self.style.SUCCESS(
            (
                f"Done. Users: {len(created_users)}, Skills: {len(created_skills)}, "
                f"SkillProgress: {len(created_progress)}, Levels: {len(created_levels)}, Rewards: {len(created_rewards)}, "
                f"AccountProgress: {len(created_account_progress)}, ActivityDays: {len(created_activity_days)}, "
                f"Streaks: {len(created_streaks)}, Events: {len(created_events)}, CourseProgress: {len(created_course_progress)}"
            )
        ))

    def _ensure_users(self, User) -> Iterable:
        created = []
        for info in DEMO_USERS:
            user, was_created = User.objects.get_or_create(
                username=info["username"],
                defaults={
                    "email": info["email"],
                    "first_name": info.get("first_name", ""),
                    "last_name": info.get("last_name", ""),
                },
            )

            if was_created:
                # Set a usable but weak password for local testing.
                try:
                    user.set_password("password")
                except Exception:
                    pass
                user.save()
                self.stdout.write(f"Created user: {user.username}")
            else:
                self.stdout.write(f"User exists: {user.username}")

            created.append(user)

        return created

    def _ensure_skills(self) -> Iterable:
        created = []
        for info in DEMO_SKILLS:
            skill, was_created = Skill.objects.get_or_create(
                name=info["name"],
                defaults={"description": info.get("description", ""), "icon_path": info.get("icon_path", "")},
            )

            if was_created:
                self.stdout.write(f"Created skill: {skill.name}")
            else:
                self.stdout.write(f"Skill exists: {skill.name}")

            created.append(skill)

        return created

    def _ensure_skill_progress(self, users: Iterable, skills: Iterable) -> Iterable:
        created = []
        # Distribute sample progress values for variety
        sample_values = [Decimal("12.5"), Decimal("45.0"), Decimal("82.3")]

        for i, user in enumerate(users):
            for j, skill in enumerate(skills):
                obj, was_created = SkillProgress.objects.get_or_create(
                    account=user,
                    skill=skill,
                    defaults={"level": 1 + ((i + j) % 3), "progress": sample_values[(i + j) % len(sample_values)]},
                )

                if was_created:
                    self.stdout.write(f"Created SkillProgress for {user.username} / {skill.name}")
                    created.append(obj)
                else:
                    self.stdout.write(f"SkillProgress exists for {user.username} / {skill.name}")

        return created

    def _ensure_level_thresholds(self) -> Iterable:
        created = []
        levels = [
            (1, 0),
            (2, 100),
            (3, 300),
            (4, 600),
            (5, 1000),
        ]

        for lvl, points in levels:
            obj, was_created = LevelThreshold.objects.get_or_create(level=lvl, defaults={"min_points": points})
            if was_created:
                self.stdout.write(f"Created LevelThreshold: level {lvl} >= {points}")
            else:
                self.stdout.write(f"LevelThreshold exists: level {lvl}")
            created.append(obj)

        return created

    def _ensure_rewards(self) -> Iterable:
        created = []
        demo_rewards = [
            ("STREAK_BONUS", 50, "Bonus for maintaining a streak"),
            ("DAILY_LOGIN", 5, "Daily login bonus"),
            ("COURSE_COMPLETION", 200, "Points for completing a course"),
        ]

        for rtype, value, desc in demo_rewards:
            obj, was_created = Reward.objects.get_or_create(reward_type=rtype, value=value, defaults={"description": desc})
            if was_created:
                self.stdout.write(f"Created Reward: {obj}")
            else:
                self.stdout.write(f"Reward exists: {obj}")
            created.append(obj)

        return created

    def _ensure_account_progress(self, users: Iterable) -> Iterable:
        created = []
        for user in users:
            obj, was_created = AccountProgress.objects.get_or_create(account=user, defaults={"point_total": 100, "level": 1})
            if was_created:
                self.stdout.write(f"Created AccountProgress for {user.username}")
            else:
                self.stdout.write(f"AccountProgress exists for {user.username}")
            created.append(obj)
        return created

    def _ensure_activity_days(self, users: Iterable) -> Iterable:
        created = []
        # create activity days for the last 3 days
        today = datetime.date.today()
        for user in users:
            for delta in range(3):
                day = today - datetime.timedelta(days=delta)
                first_at = timezone.now() - datetime.timedelta(days=delta, hours=2)
                last_at = timezone.now() - datetime.timedelta(days=delta)
                obj, was_created = AccountActivityDay.objects.get_or_create(
                    account=user,
                    activity_date=day,
                    defaults={
                        "activity_count": 1 + delta,
                        "first_activity_at": first_at,
                        "last_activity_at": last_at,
                    },
                )

                if was_created:
                    self.stdout.write(f"Created ActivityDay {day} for {user.username}")
                    created.append(obj)
                else:
                    self.stdout.write(f"ActivityDay exists {day} for {user.username}")

        return created

    def _ensure_account_streaks(self, users: Iterable) -> Iterable:
        created = []
        today = datetime.date.today()
        for user in users:
            # compute current_streak as number of consecutive recent days we created
            streak_days = AccountActivityDay.objects.filter(account=user, activity_date__gte=today - datetime.timedelta(days=6)).values_list("activity_date", flat=True)
            # simple heuristic: count consecutive days from today
            consecutive = 0
            for delta in range(0, 7):
                check = today - datetime.timedelta(days=delta)
                if check in streak_days:
                    consecutive += 1
                else:
                    break

            obj, was_created = AccountStreak.objects.get_or_create(
                account=user,
                defaults={
                    "current_streak": consecutive,
                    "longest_streak": max(consecutive, 1),
                    "last_active_date": (today if consecutive > 0 else None),
                    "last_active_at": (timezone.now() if consecutive > 0 else None),
                },
            )

            if not was_created:
                obj.current_streak = max(obj.current_streak, consecutive)
                obj.longest_streak = max(obj.longest_streak, consecutive)
                if consecutive > 0:
                    obj.last_active_date = today
                    obj.last_active_at = timezone.now()
                obj.save()
                self.stdout.write(f"Updated AccountStreak for {user.username}")
            else:
                self.stdout.write(f"Created AccountStreak for {user.username}")
                created.append(obj)

        return created

    def _ensure_reward_event_logs(self, users: Iterable, rewards: Iterable) -> Iterable:
        created = []
        now = timezone.now()
        for user in users:
            # add a daily login event and a sample reward event
            obj, was_created = RewardEventLog.objects.get_or_create(
                account=user,
                event_type="DAILY_LOGIN",
                defaults={"points_delta": 5, "created_at": now, "context": {}},
            )
            if was_created:
                self.stdout.write(f"Created RewardEventLog DAILY_LOGIN for {user.username}")
                created.append(obj)
            else:
                self.stdout.write(f"DAILY_LOGIN event exists for {user.username}")

            # sample reward event referencing first reward
            if rewards:
                reward = rewards[0]
                obj2, was_created2 = RewardEventLog.objects.get_or_create(
                    account=user,
                    event_type="REWARD_GRANTED",
                    reward=reward,
                    defaults={"points_delta": reward.value, "created_at": now, "context": {"reason": "demo"}},
                )
                if was_created2:
                    self.stdout.write(f"Created RewardEventLog REWARD_GRANTED for {user.username}")
                    created.append(obj2)
                else:
                    self.stdout.write(f"REWARD_GRANTED event exists for {user.username}")

        return created

    def _ensure_course_progress(self, users: Iterable) -> Iterable:
        created = []
        # create CourseProgress only if at least one Course exists
        course = Course.objects.first()
        if not course:
            self.stdout.write("No Course objects found — skipping CourseProgress creation")
            return created

        for i, user in enumerate(users):
            obj, was_created = CourseProgress.objects.get_or_create(
                account=user,
                course=course,
                defaults={"course_points": 10 * (i + 1), "course_level": 1, "course_progress": Decimal("12.5")},
            )
            if was_created:
                self.stdout.write(f"Created CourseProgress for {user.username} / {course}")
                created.append(obj)
            else:
                self.stdout.write(f"CourseProgress exists for {user.username} / {course}")

        return created

    def _clear_demo_data(self, User) -> None:
        # Remove SkillProgress for demo skills/users
        usernames = [u["username"] for u in DEMO_USERS]
        skill_names = [s["name"] for s in DEMO_SKILLS]

        SkillProgress.objects.filter(account__username__in=usernames, skill__name__in=skill_names).delete()
        Skill.objects.filter(name__in=skill_names).delete()
        # Optionally remove demo users
        User.objects.filter(username__in=usernames).delete()
