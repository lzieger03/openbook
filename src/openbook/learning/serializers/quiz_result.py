from __future__ import annotations

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
