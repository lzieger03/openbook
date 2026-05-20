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
from ..models.account_points        import AccountPoints

class AccountPointsSerializer(FlexFieldsModelSerializer):
    __doc__ = "Account Points"

    account = UserField()

    class Meta:
        model  = AccountPoints
        fields = ["id", "account", "point_total", "updated_at"]
        read_only_fields = ["id", "updated_at"]
        expandable_fields = {
            "account": "openbook.auth.viewsets.user.UserSerializer",
        }

class AccountPointsMeSerializer(Serializer):
    point_total = IntegerField()

class AccountPointsFilter(FilterSet):
    account = CharFilter(method="account_filter")

    class Meta:
        model  = AccountPoints
        fields = {
            "account":     [],
            "point_total": ["exact", "lte", "gte"],
            "updated_at":  ["exact", "lte", "gte"],
        }

    def account_filter(self, queryset, name, value):
        return queryset.filter(account__username=value)

@extend_schema(
    extensions={
        "x-app-name":   "Gamification",
        "x-model-name": "Account Points",
    }
)
@with_flex_fields_parameters()
class AccountPointsViewSet(ReadOnlyModelViewSet):
    __doc__ = "Current point balances per account"

    queryset         = AccountPoints.objects.select_related("account")
    serializer_class = AccountPointsSerializer
    filterset_class  = AccountPointsFilter
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
        operation_id = "gamification_account_points_me",
        summary      = "Current User Point Total",
        responses    = AccountPointsMeSerializer,
    )
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        account_points = AccountPoints.objects.get_or_create(
            account=request.user,
            defaults={"point_total": 0},
        )[0]

        return Response({"point_total": account_points.point_total})
