# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>

from django_filters.filters         import CharFilter
from django_filters.filterset       import FilterSet
from drf_spectacular.utils          import extend_schema
from rest_framework.decorators      import action
from rest_framework.response        import Response
from rest_framework.serializers     import IntegerField
from rest_framework.serializers     import Serializer
from rest_framework.viewsets        import ReadOnlyModelViewSet

from openbook.auth.serializers.user import UserField
from openbook.drf.flex_serializers  import FlexFieldsModelSerializer
from openbook.drf.viewsets          import with_flex_fields_parameters
from ..models.account_progress      import AccountProgress

class AccountProgressSerializer(FlexFieldsModelSerializer):
    __doc__ = "Account Progress"

    account = UserField()

    class Meta:
        model  = AccountProgress
        fields = ["id", "account", "point_total", "level", "updated_at"]
        read_only_fields = ["id", "updated_at"]
        expandable_fields = {
            "account": "openbook.auth.viewsets.user.UserSerializer",
        }

class AccountProgressMeSerializer(Serializer):
    point_total = IntegerField()
    level       = IntegerField()

class AccountProgressFilter(FilterSet):
    account = CharFilter(method="account_filter")

    class Meta:
        model  = AccountProgress
        fields = {
            "account":     [],
            "point_total": ["exact", "lte", "gte"],
            "level":       ["exact", "lte", "gte"],
            "updated_at":  ["exact", "lte", "gte"],
        }

    def account_filter(self, queryset, name, value):
        return queryset.filter(account__username=value)

@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Account Progress",
    }
)
@with_flex_fields_parameters()
class AccountProgressViewSet(ReadOnlyModelViewSet):
    __doc__ = "Current progress (points and level) per account"

    queryset         = AccountProgress.objects.select_related("account")
    serializer_class = AccountProgressSerializer
    filterset_class  = AccountProgressFilter
    ordering         = ["account__username"]
    search_fields    = ["account__username", "account__email"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, "user", None)

        if not user or not user.is_authenticated:
            return queryset.none()

        if user.is_staff:
            return queryset

        return queryset.filter(account=user)

    @extend_schema(
        operation_id = "gamification_account_progress_me",
        summary      = "Current User Progress",
        responses    = AccountProgressMeSerializer,
    )
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        account_progress = AccountProgress.objects.get_or_create(
            account=request.user,
            defaults={"point_total": 0, "level": 1},
        )[0]

        return Response({
            "point_total": account_progress.point_total,
            "level":       account_progress.level,
        })
