# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django_filters.filterset import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_flex_fields2.filter_backends import FlexFieldsFilterBackend
from rest_framework import serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets import with_flex_fields_parameters

from ..models.exam import ExamAttempt


class ExamAttemptSerializer(FlexFieldsModelSerializer):
    """A saved exam in the learner's history.

    Exposes the latest grading ``result`` and a *stripped* question list (no correct
    answers); the full exam (with answers) is kept server-side for re-grading only.
    """

    questions = serializers.SerializerMethodField()

    class Meta:
        model = ExamAttempt
        fields = [
            "id",
            "course",
            "textbook",
            "title",
            "questions",
            "result",
            "total_points",
            "max_points",
            "score",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
        expandable_fields = {}

    def get_questions(self, obj):
        """Client-safe question list: prompt/kind/options only, never the answers."""
        questions = (obj.exam or {}).get("questions", [])
        return [
            {
                "id": question.get("id"),
                "kind": question.get("kind"),
                "prompt": question.get("prompt"),
                "max_points": question.get("max_points", 0),
                "options": [option.get("text", "") for option in question.get("options", [])],
            }
            for question in questions
        ]


class ExamAttemptFilter(FilterSet):
    class Meta:
        model = ExamAttempt
        fields = {
            "course": ["exact"],
            "textbook": ["exact"],
        }


@extend_schema(
    extensions={
        "x-app-name": "Assistant",
        "x-model-name": "Exam Attempts",
    }
)
@with_flex_fields_parameters()
class ExamAttemptViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """The current learner's saved exams. Created server-side (via the exam WebSocket);
    here they can be listed, reviewed and deleted."""

    __doc__ = "Exam Attempts"

    serializer_class = ExamAttemptSerializer
    filterset_class = ExamAttemptFilter
    ordering = ["-updated_at"]
    search_fields = ["title"]

    # These rows are strictly private to one learner. Ownership is enforced in
    # get_queryset(), so plain authentication is enough — and we skip both the object
    # permission classes and the object-permission filter backend (which expect
    # per-object grants these rows don't have and would otherwise hide/forbid them).
    permission_classes = [IsAuthenticated]
    filter_backends = [FlexFieldsFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        # Scope strictly to the requesting user; never expose other learners' exams.
        return ExamAttempt.objects.filter(user=self.request.user)
