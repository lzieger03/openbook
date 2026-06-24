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
from openbook.content.models.course import Course
from openbook.content.models.course_material import CourseMaterial
from openbook.content.models.library_group import LibraryGroup
from openbook.content.models.textbook import Textbook
from openbook.content.models.textbook_page import TextbookPage


class CourseTextbookUpload_ViewSet_Tests(TestCase):
    """Tests for the course textbook upload action."""

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

    def test_upload_creates_material_document_and_page(self):
        """Teacher upload should create textbook content and a derived document."""
        self.client.login(username="teacher", password="password")
        file_data = SimpleUploadedFile(
            "chapter.md",
            b"# Chapter\n\nUploaded content",
            content_type="text/markdown",
        )

        response = self.client.post(
            reverse("course-upload-textbook", args=[str(self.course.id)]),
            data={"file": file_data},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        textbook = Textbook.objects.get(id=response.data["textbook"])
        material = CourseMaterial.objects.get(id=response.data["material"])
        document = AssistantDocument.objects.get(id=response.data["document"])
        page = TextbookPage.objects.get(textbook=textbook)

        self.assertEqual(textbook.name, "chapter")
        self.assertEqual(material.course, self.course)
        self.assertEqual(material.textbook, textbook)
        self.assertEqual(page.content["source"], "# Chapter\n\nUploaded content")
        self.assertEqual(document.course, self.course)
        self.assertEqual(document.textbook, textbook)
        self.assertTrue(document.file_data)
        self.assertEqual(document.index_status, AssistantDocument.IndexStatusChoices.FAILED)
        self.assertIn("MISTRAL_API_KEY", document.index_error)

    def test_upload_forbidden_without_course_change_permission(self):
        """Users without course change permission should not upload material."""
        self.client.login(username="student", password="password")
        file_data = SimpleUploadedFile("chapter.md", b"Blocked")

        response = self.client.post(
            reverse("course-upload-textbook", args=[str(self.course.id)]),
            data={"file": file_data},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Textbook.objects.exists())
        self.assertFalse(AssistantDocument.objects.exists())

    def test_upload_empty_file_denied(self):
        """Empty uploads should not create metadata-only RAG documents."""
        self.client.login(username="teacher", password="password")
        file_data = SimpleUploadedFile("empty.md", b"   ")

        response = self.client.post(
            reverse("course-upload-textbook", args=[str(self.course.id)]),
            data={"file": file_data},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Textbook.objects.exists())
        self.assertFalse(AssistantDocument.objects.exists())
