from __future__ import annotations

from rest_framework                import serializers
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from ..models.state                import LearningState


class LearningStateSerializer(FlexFieldsModelSerializer):
    class Meta:
        model  = LearningState
        fields = [
            "id",
            "user", "course", "last_page", "completed_pages",
            "is_completed", "last_accessed",
        ]
        read_only_fields = [
            "id",
            "user",
            "is_completed",
            "last_accessed",
        ]
        expandable_fields = {
            "user":            "openbook.auth.viewsets.user.UserSerializer",
            "course":          "openbook.content.viewsets.course.CourseSerializer",
            "last_page":       "openbook.content.viewsets.textbook_page.TextbookPageSerializer",
            "completed_pages": ("openbook.content.viewsets.textbook_page.TextbookPageSerializer", {"many": True}),
        }

    def get_validators(self):
        # UniqueTogetherValidator for (user, course) cannot resolve the read-only user field.
        # Uniqueness is enforced manually in validate() using the request context.
        return []

    def validate(self, data):
        request = self.context.get("request")
        if request and request.user.is_authenticated and "course" in data:
            qs = LearningState.objects.filter(user=request.user, course=data["course"])
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"course": "A learning state for this course already exists."}
                )
        return data
