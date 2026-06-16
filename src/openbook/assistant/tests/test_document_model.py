# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachada
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test import TestCase

from openbook.assistant.models.document import AssistantDocument
from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.user import User
from openbook.content.models.course import Course
from openbook.content.models.library_group import LibraryGroup


class AssistantDocument_Model_Tests(TestCase):
    """Tests for the AssistantDocument model."""

    def setUp(self):
        reset_current_user()
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

    def test_course_owner_can_manage_document(self):
        """Course owner should manage course assistant documents."""
        document = AssistantDocument.objects.create(
            course=self.course,
            title="Guide",
        )

        self.assertTrue(
            document.has_obj_perm(
                self.owner,
                "openbook_assistant.add_assistantdocument",
            )
        )
        self.assertTrue(
            document.has_obj_perm(
                self.owner,
                "openbook_assistant.change_assistantdocument",
            )
        )

    def test_unassigned_user_cannot_view_document(self):
        """Users without course access should not view course documents."""
        document = AssistantDocument.objects.create(
            course=self.course,
            title="Guide",
        )

        self.assertFalse(
            document.has_obj_perm(
                self.student,
                "openbook_assistant.view_assistantdocument",
            )
        )

    def test_index_state_methods(self):
        """Index state helpers should update status fields."""
        document = AssistantDocument(title="Guide")

        document.mark_indexing("mistral-embed")
        self.assertEqual(
            document.index_status,
            AssistantDocument.IndexStatusChoices.INDEXING,
        )
        self.assertEqual(document.embedding_model, "mistral-embed")

        document.mark_indexed(chunk_count=3)
        self.assertEqual(
            document.index_status,
            AssistantDocument.IndexStatusChoices.INDEXED,
        )
        self.assertEqual(document.chunk_count, 3)
        self.assertIsNotNone(document.indexed_at)

        document.mark_index_failed("failure")
        self.assertEqual(
            document.index_status,
            AssistantDocument.IndexStatusChoices.FAILED,
        )
        self.assertEqual(document.index_error, "failure")
        self.assertIsNone(document.indexed_at)
