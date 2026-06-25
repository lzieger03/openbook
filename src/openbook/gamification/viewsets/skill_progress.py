# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django_filters.filters import CharFilter
from django_filters.filterset import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from openbook.auth.serializers.user import UserField
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets import with_flex_fields_parameters

from ..models.skill_progress import SkillProgress


class SkillProgressSerializer(FlexFieldsModelSerializer):
    __doc__ = "Skill Progress"

    account = UserField()

    class Meta:
        model = SkillProgress
        fields = ["id", "account", "skill", "level", "progress"]
        read_only_fields = ["id"]
        expandable_fields = {
            "account": "openbook.auth.viewsets.user.UserSerializer",
            "skill": "openbook.gamification.viewsets.skill.SkillSerializer",
        }


class SkillProgressFilter(FilterSet):
    account = CharFilter(method="account_filter")

    class Meta:
        model = SkillProgress
        fields = {
            "account": [],
            "skill": ["exact"],
            "level": ["exact", "lte", "gte"],
            "progress": ["exact", "lte", "gte"],
        }

    def account_filter(self, queryset, name, value):
        return queryset.filter(account__username=value)


@extend_schema(
    extensions={
        "x-app-name": "Gamification",
        "x-model-name": "Skill Progress",
    }
)
@with_flex_fields_parameters()
class SkillProgressViewSet(ReadOnlyModelViewSet):
    __doc__ = "Current progress per skill and account"

    queryset = SkillProgress.objects.select_related("account", "skill")
    serializer_class = SkillProgressSerializer
    filterset_class = SkillProgressFilter
    ordering = ["account__username", "skill__name"]
    search_fields = ["account__username", "account__email", "skill__name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return queryset.none()

        if user.is_staff:
            return queryset

        return queryset.filter(account=user)
