from __future__ import annotations

from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from ..models.state                import LearningState


class LearningStateSerializer(FlexFieldsModelSerializer):
    class Meta:
        model  = LearningState
        fields = [
            "id",
            "user", "course", "last_page", "completed_pages",
            "last_accessed",
        ]
        read_only_fields = [
            "id",
            "user",
            "last_accessed",
        ]
        expandable_fields = {
            "user":            "openbook.auth.viewsets.user.UserSerializer",
            "course":          "openbook.content.viewsets.course.CourseSerializer",
            "last_page":       "openbook.content.viewsets.textbook_page.TextbookPageSerializer",
            "completed_pages": ("openbook.content.viewsets.textbook_page.TextbookPageSerializer", {"many": True}),
        }
