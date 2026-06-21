from __future__ import annotations

from django_filters.filterset              import FilterSet
from drf_spectacular.utils                 import extend_schema
from django_filters.rest_framework         import DjangoFilterBackend
from rest_framework.filters                import OrderingFilter, SearchFilter
from rest_framework.viewsets               import ModelViewSet
from rest_flex_fields2.filter_backends     import FlexFieldsFilterBackend

from openbook.drf.viewsets          import ModelViewSetMixin, with_flex_fields_parameters
from openbook.drf.flex_serializers  import FlexFieldsModelSerializer
from ..models.state                 import LearningState
from ..serializers.state            import LearningStateSerializer


class LearningStateFilter(FilterSet):
    class Meta:
        model  = LearningState
        fields = {
            "user":   ["exact"],
            "course": ["exact"],
        }


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
