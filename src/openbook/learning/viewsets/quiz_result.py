from __future__ import annotations

from django_filters.filterset              import FilterSet
from drf_spectacular.utils                 import extend_schema
from django_filters.rest_framework         import DjangoFilterBackend
from rest_framework.filters                import OrderingFilter, SearchFilter
from rest_framework.viewsets               import ModelViewSet
from rest_flex_fields2.filter_backends     import FlexFieldsFilterBackend

from openbook.drf.viewsets         import ModelViewSetMixin, with_flex_fields_parameters
from ..models.quiz_result          import QuizResult
from ..serializers.quiz_result     import QuizResultSerializer


class QuizResultFilter(FilterSet):
    class Meta:
        model  = QuizResult
        fields = {
            "user":  ["exact"],
            "page":  ["exact"],
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
