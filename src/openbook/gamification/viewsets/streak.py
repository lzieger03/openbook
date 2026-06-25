# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from drf_spectacular.utils      import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response
from rest_framework.serializers import ChoiceField
from rest_framework.serializers import DateField
from rest_framework.serializers import DateTimeField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import JSONField
from rest_framework.serializers import Serializer
from rest_framework.viewsets    import ViewSet

from ..constants        import LearningActivityType
from ..services.streak  import get_streak_state, record_learning_activity


class StreakStateSerializer(Serializer):
    __doc__ = "Current daily streak state of an account"

    current_streak   = IntegerField()
    longest_streak   = IntegerField()
    last_active_date = DateField(allow_null=True)
    streak_freezes   = IntegerField()


class RecordActivityRequestSerializer(Serializer):
    __doc__ = "Record a learning activity"

    activity_type = ChoiceField(choices=LearningActivityType.choices)
    occurred_at   = DateTimeField(required=False)
    metadata      = JSONField(required=False)


@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Activity",
    }
)
class ActivityViewSet(ViewSet):
    __doc__ = "Record real learning activities that may advance the daily streak"

    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id = "gamification_activity_record",
        summary      = "Record Learning Activity",
        request      = RecordActivityRequestSerializer,
        responses    = StreakStateSerializer,
    )
    def create(self, request):
        serializer = RecordActivityRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        state = record_learning_activity(
            account_id    = request.user.id,
            activity_type = serializer.validated_data["activity_type"],
            occurred_at   = serializer.validated_data.get("occurred_at"),
            metadata      = serializer.validated_data.get("metadata"),
        )

        return Response(StreakStateSerializer(state).data, status=201)


@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Streak",
    }
)
class StreakViewSet(ViewSet):
    __doc__ = "Daily learning streak of the current user"

    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id = "gamification_streak_retrieve",
        summary      = "Current User Streak",
        responses    = StreakStateSerializer,
    )
    def list(self, request):
        state = get_streak_state(request.user.id)
        return Response(StreakStateSerializer(state).data)
