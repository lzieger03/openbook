# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from openbook.auth.serializers.user import UserField
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets import with_flex_fields_parameters

from ..models.course_progress import CourseProgress


class CourseProgressSerializer(FlexFieldsModelSerializer):
    __doc__ = "Course Progress"

    account = UserField()

    class Meta:
        model = CourseProgress
        fields = ["id", "account", "course", "course_points", "course_level", "course_progress"]
        read_only_fields = ["id"]
        expandable_fields = {
            "account": "openbook.auth.viewsets.user.UserSerializer",
            "course": "openbook.content.viewsets.course.CourseSerializer",
        }


class CourseProgressFilter(FilterSet):
    account = CharFilter(method="account_filter")

    class Meta:
        model = CourseProgress
        fields = {
            "account": [],
            "course": ["exact"],
            "course_points": ["exact", "lte", "gte"],
            "course_level": ["exact", "lte", "gte"],
            "course_progress": ["exact", "lte", "gte"],
        }

    def account_filter(self, queryset, name, value):
        return queryset.filter(account__username=value)


@extend_schema(
    extensions={
        "x-app-name": "Gamification",
        "x-model-name": "Course Progress",
    }
)
@with_flex_fields_parameters()
class CourseProgressViewSet(ReadOnlyModelViewSet):
    __doc__ = "Current progress per course and account"

    queryset = CourseProgress.objects.select_related("account", "course")
    serializer_class = CourseProgressSerializer
    filterset_class = CourseProgressFilter
    ordering = ["account__username", "course__name"]
    search_fields = ["account__username", "account__email", "course__name", "course__slug"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return queryset.none()

        if user.is_staff:
            return queryset

        return queryset.filter(account=user)
