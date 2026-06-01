# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django_filters.filterset import FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets import with_flex_fields_parameters

from ..models.skill import Skill


class SkillSerializer(FlexFieldsModelSerializer):
    __doc__ = "Skill"

    class Meta:
        model = Skill
        fields = ["id", "name", "description", "icon_path"]
        read_only_fields = ["id"]
        expandable_fields = {}


class SkillFilter(FilterSet):
    class Meta:
        model = Skill
        fields = {
            "name": ["exact", "icontains"],
            "icon_path": ["exact", "icontains"],
        }


@extend_schema(
    extensions={
        "x-app-name": "Gamification",
        "x-model-name": "Skill",
    }
)
@with_flex_fields_parameters()
class SkillViewSet(ReadOnlyModelViewSet):
    __doc__ = "Global skill catalog"

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_class = SkillFilter
    ordering = ["name"]
    search_fields = ["name", "description"]
