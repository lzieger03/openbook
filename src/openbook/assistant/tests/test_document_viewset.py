# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from openbook.assistant.models.document import AssistantDocument
from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.user import User
from openbook.auth.utils import permission_for_perm_string
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup


class AssistantDocument_ViewSet_Tests(TestCase):
    """Tests for the AssistantDocumentViewSet REST API."""

    def setUp(self):
        reset_current_user()
        self.media_dir = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(
            MEDIA_ROOT=self.media_dir.name,
            MISTRAL_API_KEY="",
        )
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(self.media_dir.cleanup)

        self.client = APIClient()
        self.owner = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="password",
        )
        self.student = User.objects.create_user(
            username="student",
            email="student@example.com",
            password="password",
        )
        self.library_group = LibraryGroup.objects.create(name="Library", slug="library")
        self.course = Course.objects.create(
            name="Course",
            slug="course",
            group=self.library_group,
            owner=self.owner,
        )
        self.course.public_permissions.add(
            permission_for_perm_string("openbook_content.view_course")
        )
        self.document = AssistantDocument.objects.create(
            course=self.course,
            title="Guide",
        )

    def test_list_visible_with_course_view_permission(self):
        """Course viewers should list course assistant documents."""
        self.client.login(username="student", password="password")

        response = self.client.get(
            reverse("assistant-document-list"),
            query_params={"course": str(self.course.id)},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], str(self.document.id))

    def test_create_ok_for_course_owner(self):
        """Course owner should upload assistant documents."""
        self.client.login(username="teacher", password="password")
        file_data = SimpleUploadedFile("guide.txt", b"Hello")

        response = self.client.post(
            reverse("assistant-document-list"),
            data={
                "course": str(self.course.id),
                "title": "Uploaded guide",
                "file_data": file_data,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        document = AssistantDocument.objects.get(title="Uploaded guide")
        self.assertEqual(document.course, self.course)
        self.assertEqual(
            document.index_status,
            AssistantDocument.IndexStatusChoices.FAILED,
        )
        self.assertIn("MISTRAL_API_KEY", document.index_error)

    def test_create_forbidden_for_course_viewer(self):
        """Course viewers without change permission should not upload documents."""
        self.client.login(username="student", password="password")
        file_data = SimpleUploadedFile("guide.txt", b"Hello")

        response = self.client.post(
            reverse("assistant-document-list"),
            data={
                "course": str(self.course.id),
                "title": "Blocked guide",
                "file_data": file_data,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(AssistantDocument.objects.filter(title="Blocked guide").exists())
