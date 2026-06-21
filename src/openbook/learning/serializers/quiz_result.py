from __future__ import annotations

from rest_framework                import serializers
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from ..models.quiz_result          import QuizResult


class QuizResultSerializer(FlexFieldsModelSerializer):
    class Meta:
        model  = QuizResult
        fields = [
            "id",
            "user", "page",
            "score", "attempts",
            "answered_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "answered_at",
        ]
        expandable_fields = {
            "user": "openbook.auth.viewsets.user.UserSerializer",
            "page": "openbook.content.viewsets.textbook_page.TextbookPageSerializer",
        }

    def get_validators(self):
        # UniqueTogetherValidator for (user, page) cannot resolve the read-only user field.
        # Uniqueness is enforced manually in validate() using the request context.
        return []

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user.is_authenticated and "page" in data:
            qs = QuizResult.objects.filter(user=request.user, page=data["page"])
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"page": "A quiz result for this page already exists."}
                )
        return data
