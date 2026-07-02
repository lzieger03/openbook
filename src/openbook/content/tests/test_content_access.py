# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth                   import get_user_model
from django.contrib.auth.models            import Permission
from django.contrib.contenttypes.models    import ContentType
from django.test                           import TestCase
from django.urls                           import reverse
from rest_framework.test                   import APIClient

from openbook.auth.middleware.current_user import reset_current_user
from openbook.auth.models.anonymous_permission import AnonymousPermission

from ..models.course               import Course
from ..models.course_material      import CourseMaterial
from ..models.course_material      import CourseMaterialPageRange
from ..models.library_group        import LibraryGroup
from ..models.textbook             import Textbook
from ..models.textbook_page        import TextbookPage

User = get_user_model()


class CourseContentAccessTests(TestCase):
    """
    A learner (a plain authenticated user without explicit permissions) must be able
    to read the course content authored in the teacher area, so it can be shown on the
    dashboard. The course material, page range and textbook page endpoints are
    therefore list/retrieve readable, just like the textbook endpoint.
    """

    def setUp(self):
        super().setUp()
        reset_current_user()
        self.client = APIClient()

        self.grant_anonymous_view("openbook_content", "coursematerial", "view_coursematerial")
        self.grant_anonymous_view("openbook_content", "coursematerialpagerange", "view_coursematerialpagerange")
        self.grant_anonymous_view("openbook_content", "textbookpage", "view_textbookpage")

        self.library_group = LibraryGroup.objects.create(name="Group", slug="group")
        self.course = Course.objects.create(name="Course", slug="course", group=self.library_group)
        self.textbook = Textbook.objects.create(name="Book", slug="book", group=self.library_group)

        self.page_one = TextbookPage.objects.create(
            textbook=self.textbook,
            name="Page 1",
            position=1,
            content={"type": "source", "format": "MD", "source": "# Hello"},
        )
        self.page_two = TextbookPage.objects.create(
            textbook=self.textbook,
            name="Page 2",
            position=2,
            content={"type": "source", "format": "MD", "source": "## World"},
        )

        self.material = CourseMaterial.objects.create(
            course=self.course,
            textbook=self.textbook,
            position=1,
        )
        self.page_range = CourseMaterialPageRange.objects.create(
            material=self.material,
            start_page=self.page_one,
            end_page=self.page_two,
            position=1,
        )

        # A plain learner: authenticated but without any model/object permissions.
        self.learner = User.objects.create_user(
            username="learner",
            email="learner@test.com",
            password="password",
        )

    def grant_anonymous_view(self, app_label, model, codename):
        """Grant a global object-level view permission, as the fixture does at runtime."""
        content_type = ContentType.objects.get(app_label=app_label, model=model)
        permission = Permission.objects.get(content_type=content_type, codename=codename)
        AnonymousPermission.objects.get_or_create(permission=permission)

    def login_as_learner(self):
        reset_current_user()
        self.client.logout()
        self.client.login(username="learner", password="password")

    def test_learner_can_read_course_materials(self):
        """A user without permissions can list a course's materials."""
        self.login_as_learner()

        response = self.client.get(reverse("course-material-list"), {"course": str(self.course.id)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_learner_can_read_page_ranges(self):
        """A user without permissions can list a material's page ranges."""
        self.login_as_learner()

        response = self.client.get(
            reverse("course-material-page-range-list"),
            {"material": str(self.material.id)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_learner_can_read_textbook_pages(self):
        """A user without permissions can list (and read the content of) textbook pages."""
        self.login_as_learner()

        response = self.client.get(reverse("textbook-page-list"), {"textbook": str(self.textbook.id)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    @patch("openbook.content.viewsets.textbook_page.TextbookDocumentSyncService")
    def test_teacher_can_delete_textbook_page(self, sync_service_cls):
        """Deleting a textbook page should remove it and resync the textbook document."""
        teacher = User.objects.create_superuser(
            username="teacher",
            email="teacher@test.com",
            password="password",
        )
        self.client.force_authenticate(teacher)

        response = self.client.delete(
            reverse("textbook-page-detail", args=[self.page_one.id]),
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(TextbookPage.objects.filter(pk=self.page_one.pk).exists())
        sync_service_cls.return_value.sync_textbook.assert_called_once_with(self.textbook)
