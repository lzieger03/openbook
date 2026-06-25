# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django_filters.filters        import CharFilter
from django_filters.filterset      import FilterSet
from drf_spectacular.utils         import extend_schema
from rest_framework.viewsets       import ReadOnlyModelViewSet

from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets         import with_flex_fields_parameters
from ..models.reward               import Reward

class RewardSerializer(FlexFieldsModelSerializer):
    __doc__ = "Reward"

    class Meta:
        model  = Reward
        fields = ["id", "reward_type", "value", "description"]
        expandable_fields = {}

class RewardFilter(FilterSet):
    reward_type = CharFilter(lookup_expr="icontains")

    class Meta:
        model  = Reward
        fields = {
            "reward_type": ["exact", "icontains"],
            "value":       ["exact", "lte", "gte"],
        }

@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Rewards",
    }
)
@with_flex_fields_parameters()
class RewardViewSet(ReadOnlyModelViewSet):
    __doc__ = "Rewards"

    queryset         = Reward.objects.all()
    serializer_class = RewardSerializer
    filterset_class  = RewardFilter
    ordering         = ["reward_type", "value"]
    search_fields    = ["reward_type", "description"]
