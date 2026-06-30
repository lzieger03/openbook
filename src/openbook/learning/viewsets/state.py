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

from openbook.content.models.course        import Course
from openbook.content.models.textbook_page import TextbookPage
from openbook.drf.viewsets                 import ModelViewSetMixin, with_flex_fields_parameters
from ..models.state                        import LearningState
from ..serializers.state                   import LearningStateSerializer
from ..services                            import LearningActivityService


class LearningStateFilter(FilterSet):
    class Meta:
        model  = LearningState
        fields = {
            "user":   ["exact"],
            "course": ["exact"],
        }


class _PageActionSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    page   = serializers.PrimaryKeyRelatedField(queryset=TextbookPage.objects.all())


class _CourseActionSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())


@extend_schema(
    extensions={
        "x-app-name":   "Learning",
        "x-model-name": "Learning States",
    }
)
@with_flex_fields_parameters()
class LearningStateViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Learning States"

    queryset         = LearningState.objects.all()
    serializer_class = LearningStateSerializer
    filterset_class  = LearningStateFilter
    ordering         = ["-last_accessed"]
    search_fields    = []

    # Ownership is enforced via get_queryset(); object-permission filter is not needed
    filter_backends = [FlexFieldsFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(request=_PageActionSerializer, responses={200: LearningStateSerializer})
    @action(detail=False, methods=["post"], url_path="record-page-opened")
    def record_page_opened(self, request):
        s = _PageActionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        course = s.validated_data["course"]
        page   = s.validated_data["page"]

        try:
            state = LearningActivityService().record_page_opened(
                user=request.user,
                course=course,
                page=page,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc

        return Response(LearningStateSerializer(state, context={"request": request}).data)

    @extend_schema(request=_PageActionSerializer, responses={200: LearningStateSerializer})
    @action(detail=False, methods=["post"], url_path="mark-page-completed")
    def mark_page_completed(self, request):
        s = _PageActionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        course = s.validated_data["course"]
        page   = s.validated_data["page"]

        try:
            state = LearningActivityService().mark_page_completed(
                user=request.user,
                course=course,
                page=page,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages) from exc

        return Response(LearningStateSerializer(state, context={"request": request}).data)

    @extend_schema(request=_CourseActionSerializer, responses={200: LearningStateSerializer})
    @action(detail=False, methods=["post"], url_path="complete-course")
    def complete_course(self, request):
        s = _CourseActionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        course = s.validated_data["course"]

        state, _ = LearningState.objects.get_or_create(user=request.user, course=course)
        if not state.is_completed:
            state.is_completed = True
            state.save()

            from openbook.gamification.services.course import award_course_points
            award_course_points(request.user.id, course.id, 200)

        return Response(LearningStateSerializer(state, context={"request": request}).data)
