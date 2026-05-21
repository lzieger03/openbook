# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from .viewsets.account_points import AccountPointsViewSet
from .viewsets.reward import RewardViewSet
from .viewsets.reward_event import RewardEventViewSet


def register_api_routes(router, prefix):
    """
    Register gamification API routes.
    """
    router.register(
        f"{prefix}/account_points",
        AccountPointsViewSet,
        basename="account_points",
    )
    router.register(
        f"{prefix}/rewards",
        RewardViewSet,
        basename="reward",
    )
    router.register(
        f"{prefix}/reward_events",
        RewardEventViewSet,
        basename="reward_event",
    )
