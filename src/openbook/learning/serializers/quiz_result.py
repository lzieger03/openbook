from __future__ import annotations

from rest_framework                import serializers
from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from ..models.quiz_result          import QuizResult


class QuizResultSerializer(FlexFieldsModelSerializer):
    class Meta:
        model  = QuizResult
        fields = [
            "id",
            "user",
            "course",
            "textbook",
            "page",
            "activity_type",
            "score",
            "attempts",
            "metadata",
            "answered_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "answered_at",
        ]
        expandable_fields = {
            "user": "openbook.auth.viewsets.user.UserSerializer",
            "course": "openbook.content.viewsets.course.CourseSerializer",
            "textbook": "openbook.content.viewsets.textbook.TextbookSerializer",
            "page": "openbook.content.viewsets.textbook_page.TextbookPageSerializer",
        }

    def get_validators(self):
        # UniqueTogetherValidator for (user, page) cannot resolve the read-only user field.
        # Uniqueness is enforced manually in validate() using the request context.
        return []

    def validate(self, data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return data

        activity_type = data.get(
            "activity_type",
            self.instance.activity_type if self.instance else QuizResult.ActivityTypeChoices.QUIZ,
        )
        page = data.get("page", self.instance.page if self.instance else None)
        course = data.get("course", self.instance.course if self.instance else None)

        if page:
            qs = QuizResult.objects.filter(
                user=request.user,
                page=page,
                activity_type=activity_type,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"page": "An activity result for this page already exists."}
                )

        if not page and course:
            qs = QuizResult.objects.filter(
                user=request.user,
                course=course,
                page__isnull=True,
                activity_type=activity_type,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"course": "An activity result for this course already exists."}
                )

        return data
