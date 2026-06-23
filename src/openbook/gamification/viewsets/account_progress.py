# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django_filters.filters         import CharFilter
from django_filters.filterset       import FilterSet
from drf_spectacular.utils          import extend_schema
from rest_framework.decorators      import action
from rest_framework.response        import Response
from rest_framework.serializers     import BooleanField
from rest_framework.serializers     import CharField
from rest_framework.serializers     import IntegerField
from rest_framework.serializers     import Serializer
from rest_framework.viewsets        import ReadOnlyModelViewSet

from openbook.auth.serializers.user import UserField
from openbook.drf.flex_serializers  import FlexFieldsModelSerializer
from openbook.drf.viewsets          import with_flex_fields_parameters
from ..models.account_progress      import AccountProgress
from ..models.level_threshold       import LevelThreshold

class AccountProgressSerializer(FlexFieldsModelSerializer):
    __doc__ = "Account Progress"

    account = UserField()

    class Meta:
        model  = AccountProgress
        fields = ["id", "account", "point_total", "level", "updated_at"]
        read_only_fields = ["id", "updated_at"]
        expandable_fields = {
            "account": "openbook.auth.viewsets.user.UserSerializer",
        }

class AccountProgressMeSerializer(Serializer):
    point_total              = IntegerField()
    level                    = IntegerField()
    current_level_min_points = IntegerField()
    next_level_min_points    = IntegerField(allow_null=True)

class LeaderboardEntrySerializer(Serializer):
    rank            = IntegerField()
    username        = CharField()
    full_name       = CharField()
    level           = IntegerField()
    point_total     = IntegerField()
    is_current_user = BooleanField()

class AccountProgressFilter(FilterSet):
    account = CharFilter(method="account_filter")

    class Meta:
        model  = AccountProgress
        fields = {
            "account":     [],
            "point_total": ["exact", "lte", "gte"],
            "level":       ["exact", "lte", "gte"],
            "updated_at":  ["exact", "lte", "gte"],
        }

    def account_filter(self, queryset, name, value):
        return queryset.filter(account__username=value)

@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Account Progress",
    }
)
@with_flex_fields_parameters()
class AccountProgressViewSet(ReadOnlyModelViewSet):
    __doc__ = "Current progress (points and level) per account"

    queryset         = AccountProgress.objects.select_related("account")
    serializer_class = AccountProgressSerializer
    filterset_class  = AccountProgressFilter
    ordering         = ["account__username"]
    search_fields    = ["account__username", "account__email"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return queryset.none()

        if user.is_staff:
            return queryset

        return queryset.filter(account=user)

    @extend_schema(
        operation_id = "gamification_account_progress_me",
        summary      = "Current User Progress",
        responses    = AccountProgressMeSerializer,
    )
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        account_progress = AccountProgress.objects.get_or_create(
            account=request.user,
            defaults={"point_total": 0, "level": 1},
        )[0]

        level = account_progress.level

        # Point bounds of the current level so the client can render a
        # "progress towards the next level" bar that resets on each level-up.
        current_threshold = (
            LevelThreshold.objects
            .filter(level__lte=level)
            .order_by("-level")
            .first()
        )
        next_threshold = (
            LevelThreshold.objects
            .filter(level__gt=level)
            .order_by("level")
            .first()
        )

        return Response({
            "point_total":              account_progress.point_total,
            "level":                    level,
            "current_level_min_points": current_threshold.min_points if current_threshold else 0,
            "next_level_min_points":    next_threshold.min_points if next_threshold else None,
        })

    @extend_schema(
        operation_id = "gamification_account_progress_leaderboard",
        summary      = "Leaderboard",
        responses    = LeaderboardEntrySerializer(many=True),
    )
    @action(detail=False, methods=["get"], url_path="leaderboard")
    def leaderboard(self, request):
        # The leaderboard is global: every authenticated user sees the same
        # ranking, so query all accounts directly rather than the (per-user
        # scoped) default queryset.
        top = (
            AccountProgress.objects
            .select_related("account")
            .order_by("-point_total", "account__username")[:10]
        )

        entries = [
            {
                "rank":            index,
                "username":        progress.account.username,
                "full_name":       progress.account.get_full_name() or progress.account.username,
                "level":           progress.level,
                "point_total":     progress.point_total,
                "is_current_user": progress.account_id == request.user.id,
            }
            for index, progress in enumerate(top, start=1)
        ]

        return Response(entries)
