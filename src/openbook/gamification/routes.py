# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from .viewsets.account_progress import AccountProgressViewSet
from .viewsets.reward import RewardViewSet
from .viewsets.reward_event_log import RewardEventLogViewSet
from .viewsets.streak import ActivityViewSet, StreakViewSet


def register_api_routes(router, prefix):
    """
    Register gamification API routes.
    """
    router.register(
        f"{prefix}/account_progress",
        AccountProgressViewSet,
        basename="account_progress",
    )
    router.register(
        f"{prefix}/rewards",
        RewardViewSet,
        basename="reward",
    )
    router.register(
        f"{prefix}/reward_event_log",
        RewardEventLogViewSet,
        basename="reward_event_log",
    )
    router.register(
        f"{prefix}/activity",
        ActivityViewSet,
        basename="activity",
    )
    router.register(
        f"{prefix}/streak",
        StreakViewSet,
        basename="streak",
    )
