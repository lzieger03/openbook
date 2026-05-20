# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django_filters.filters         import CharFilter
from django_filters.filterset       import FilterSet
from drf_spectacular.utils          import extend_schema
from rest_framework.decorators      import action
from rest_framework.response        import Response
from rest_framework.serializers     import CharField
from rest_framework.serializers     import IntegerField
from rest_framework.serializers     import JSONField
from rest_framework.serializers     import PrimaryKeyRelatedField
from rest_framework.serializers     import Serializer
from rest_framework.serializers     import ValidationError
from rest_framework.viewsets        import ReadOnlyModelViewSet

from openbook.auth.serializers.user import UserField
from openbook.drf.flex_serializers  import FlexFieldsModelSerializer
from openbook.drf.viewsets          import with_flex_fields_parameters
from ..models.account_points        import AccountPoints
from ..models.reward                import Reward
from ..models.reward_event          import RewardEvent

class RewardEventSerializer(FlexFieldsModelSerializer):
    __doc__ = "Reward Event"

    account = UserField()

    class Meta:
        model  = RewardEvent
        fields = [
            "id", "account", "reward", "event_type",
            "points_delta", "created_at", "context",
        ]
        read_only_fields = ["id", "created_at"]
        expandable_fields = {
            "account": "openbook.auth.viewsets.user.UserSerializer",
            "reward":  "openbook.gamification.viewsets.reward.RewardSerializer",
        }

class RewardEventFilter(FilterSet):
    account    = CharFilter(method="account_filter")
    event_type = CharFilter(lookup_expr="icontains")

    class Meta:
        model  = RewardEvent
        fields = {
            "account":      [],
            "reward":       ["exact"],
            "event_type":   ["exact", "icontains"],
            "points_delta": ["exact", "lte", "gte"],
            "created_at":   ["exact", "lte", "gte"],
        }

    def account_filter(self, queryset, name, value):
        return queryset.filter(account__username=value)

class TriggerRewardEventRequestSerializer(Serializer):
    account    = UserField(required=False)
    reward     = PrimaryKeyRelatedField(queryset=Reward.objects.all())
    event_type = CharField(max_length=64, required=False, allow_blank=True)
    context    = JSONField(required=False)

class TriggerRewardEventResponseSerializer(Serializer):
    reward_event = RewardEventSerializer()
    point_total  = IntegerField()

@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Reward Events",
    }
)
@with_flex_fields_parameters()
class RewardEventViewSet(ReadOnlyModelViewSet):
    __doc__ = "Reward events (audit log)"

    queryset         = RewardEvent.objects.select_related("account", "reward")
    serializer_class = RewardEventSerializer
    filterset_class  = RewardEventFilter
    ordering         = ["-created_at"]
    search_fields    = ["account__username", "event_type", "reward__reward_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return queryset.none()

        if user.is_staff:
            return queryset

        return queryset.filter(account=user)

    @extend_schema(
        operation_id = "gamification_reward_event_trigger",
        summary      = "Trigger Reward Event",
        request      = TriggerRewardEventRequestSerializer,
        responses    = TriggerRewardEventResponseSerializer,
    )
    @action(detail=False, methods=["post"], url_path="trigger")
    def trigger(self, request):
        serializer = TriggerRewardEventRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data.get("account", request.user)

        if account != request.user and not request.user.is_staff:
            raise ValidationError({
                "account": "Only staff users can trigger reward events for other accounts.",
            })

        reward = serializer.validated_data["reward"]
        context = serializer.validated_data.get("context", {})
        event_type = serializer.validated_data.get("event_type") or reward.reward_type

        reward_event = RewardEvent.objects.create(
            account=account,
            reward=reward,
            event_type=event_type,
            points_delta=reward.value,
            context=context,
        )

        account_points = AccountPoints.objects.get_or_create(
            account=account,
            defaults={"point_total": 0},
        )[0]

        response_serializer = TriggerRewardEventResponseSerializer(
            {
                "reward_event": reward_event,
                "point_total": account_points.point_total,
            }
        )

        return Response(response_serializer.data, status=201)
