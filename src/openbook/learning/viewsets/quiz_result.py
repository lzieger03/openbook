from __future__ import annotations

from django.core.exceptions                 import ValidationError as DjangoValidationError
from django_filters.filterset              import FilterSet
from drf_spectacular.utils                 import extend_schema
from django_filters.rest_framework         import DjangoFilterBackend
from rest_framework                        import serializers
from rest_framework.decorators             import action
from rest_framework.filters                import OrderingFilter, SearchFilter
from rest_framework.response               import Response
from rest_framework.viewsets               import ModelViewSet
from rest_flex_fields2.filter_backends     import FlexFieldsFilterBackend

from openbook.content.models       import Course
from openbook.content.models       import Textbook
from openbook.content.models       import TextbookPage
from openbook.drf.viewsets         import ModelViewSetMixin, with_flex_fields_parameters
from ..models.quiz_result          import QuizResult
from ..serializers.quiz_result     import QuizResultSerializer
from ..services                    import LearningActivityService


class _ActivityResultActionSerializer(serializers.Serializer):
    course        = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    activity_type = serializers.ChoiceField(choices=QuizResult.ActivityTypeChoices.choices)
    score         = serializers.FloatField(min_value=0.0, max_value=1.0)
    page          = serializers.PrimaryKeyRelatedField(
        queryset=TextbookPage.objects.all(),
        required=False,
        allow_null=True,
    )
    textbook      = serializers.PrimaryKeyRelatedField(
        queryset=Textbook.objects.all(),
        required=False,
        allow_null=True,
    )
    attempts      = serializers.IntegerField(min_value=1, required=False)
    metadata      = serializers.JSONField(required=False)


class QuizResultFilter(FilterSet):
    class Meta:
        model  = QuizResult
        fields = {
            "user":          ["exact"],
            "course":        ["exact"],
            "textbook":      ["exact"],
            "page":          ["exact"],
            "activity_type": ["exact"],
        }


@extend_schema(
    extensions={
        "x-app-name":   "Learning",
        "x-model-name": "Quiz Results",
    }
)
@with_flex_fields_parameters()
class QuizResultViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Quiz Results"

    queryset         = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    filterset_class  = QuizResultFilter
    ordering         = ["-answered_at"]
    search_fields    = []

    # Ownership is enforced via get_queryset(); object-permission filter is not needed
    filter_backends = [FlexFieldsFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        request=_ActivityResultActionSerializer,
        responses={200: QuizResultSerializer},
        operation_id="learning_quiz_results_record_activity",
        summary="Record or update a learning activity result.",
    )
    @action(detail=False, methods=["post"], url_path="record-activity")
    def record_activity(self, request):
        serializer = _ActivityResultActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = LearningActivityService().record_activity_result(
                user=request.user,
                course=data["course"],
                activity_type=data["activity_type"],
                score=data["score"],
                page=data.get("page"),
                textbook=data.get("textbook"),
                attempts=data.get("attempts"),
                metadata=data.get("metadata"),
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc

        return Response(QuizResultSerializer(result, context={"request": request}).data)
