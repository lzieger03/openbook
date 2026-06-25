# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import typing

from .viewsets.document import AssistantDocumentViewSet
from .viewsets.exam_attempt import ExamAttemptViewSet

if typing.TYPE_CHECKING:
    from rest_framework.routers import DefaultRouter


def register_api_routes(router: "DefaultRouter", prefix: str) -> None:
    router.register(
        f"{prefix}/documents",
        AssistantDocumentViewSet,
        basename="assistant-document",
    )
    router.register(
        f"{prefix}/exam_attempts",
        ExamAttemptViewSet,
        basename="assistant-exam-attempt",
    )
