# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import CharField
from rest_framework.serializers import DecimalField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import JSONField
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet

from openbook.auth.serializers.user import UserField
from openbook.content.models.course import Course
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets import with_flex_fields_parameters

from ..models.account_progress import AccountProgress
from ..models.course_progress import CourseProgress
from ..models.skill import Skill
from ..services.course import award_course_points
from ..services.skill import award_skill_progress


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


class AwardCoursePointsRequestSerializer(Serializer):
    account      = UserField(required=False)
    course       = PrimaryKeyRelatedField(queryset=Course.objects.all())
    points       = IntegerField()
    # Optionally also advance skills. ``skill`` targets one specific skill (e.g. the
    # skill a quiz question trains); when omitted, every skill the course teaches is
    # advanced. ``skill_points`` is the progress (in %) added per skill; it defaults
    # to the course ``points`` when not given.
    skill        = PrimaryKeyRelatedField(queryset=Skill.objects.all(), required=False)
    skill_points = IntegerField(required=False)
    context      = JSONField(required=False)


class AwardedSkillSerializer(Serializer):
    skill          = CharField()
    skill_level    = IntegerField()
    skill_progress = DecimalField(max_digits=5, decimal_places=2)


class AwardCoursePointsResponseSerializer(Serializer):
    course          = CharField()
    course_points   = IntegerField()
    course_level    = IntegerField()
    course_progress = DecimalField(max_digits=5, decimal_places=2)
    point_total     = IntegerField()
    level           = IntegerField()
    skills          = AwardedSkillSerializer(many=True)


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

    @extend_schema(
        operation_id = "gamification_course_progress_award",
        summary      = "Award Course Points",
        request      = AwardCoursePointsRequestSerializer,
        responses    = AwardCoursePointsResponseSerializer,
    )
    @action(detail=False, methods=["post"], url_path="award")
    def award(self, request):
        """
        Award points to a learner inside a course. Updates the per-course progress
        (points, level and the progress bar) and feeds the same points into the
        global level and point system.
        """
        serializer = AwardCoursePointsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data.get("account", request.user)

        if account != request.user and not request.user.is_staff:
            raise ValidationError({
                "account": "Only staff users can award course points to other accounts.",
            })

        course       = serializer.validated_data["course"]
        points       = serializer.validated_data["points"]
        skill        = serializer.validated_data.get("skill")
        skill_points = serializer.validated_data.get("skill_points", points)
        context      = serializer.validated_data.get("context", {})

        try:
            state = award_course_points(account.id, course.id, points, context=context)
        except ValueError as error:
            raise ValidationError({"points": str(error)})

        # Advance the skills trained in this course. A specific skill (e.g. the one a
        # quiz question targets) takes precedence; otherwise every skill the course
        # teaches grows. Skipped silently when nothing to award.
        target_skills = [skill] if skill else list(course.skills.all())
        awarded_skills = []

        if skill_points > 0:
            for target in target_skills:
                skill_state = award_skill_progress(account.id, target.id, skill_points)
                awarded_skills.append({
                    "skill":          target.name,
                    "skill_level":    skill_state["skill_level"],
                    "skill_progress": skill_state["skill_progress"],
                })

        account_progress = AccountProgress.objects.get_or_create(
            account=account,
            defaults={"point_total": 0, "level": 1},
        )[0]

        return Response(
            {
                "course":          course.name,
                "course_points":   state["course_points"],
                "course_level":    state["course_level"],
                "course_progress": state["course_progress"],
                "point_total":     account_progress.point_total,
                "level":           account_progress.level,
                "skills":          awarded_skills,
            },
            status=201,
        )
