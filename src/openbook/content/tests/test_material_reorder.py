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

from django.contrib.auth                   import get_user_model
from django.test                           import TestCase
from django.urls                           import reverse
from rest_framework.test                   import APIClient

from openbook.auth.middleware.current_user import reset_current_user

from ..models.course               import Course
from ..models.course_material      import CourseMaterial
from ..models.library_group        import LibraryGroup
from ..models.textbook             import Textbook

User = get_user_model()


class CourseMaterialReorderTests(TestCase):
    """
    The ``move`` action swaps a material with its neighbour. A naive swap of the two
    ``position`` values would violate the unique ``(course, position)`` constraint, so
    the endpoint must perform the swap atomically and succeed.
    """

    def setUp(self):
        super().setUp()
        reset_current_user()
        self.client = APIClient()

        self.library_group = LibraryGroup.objects.create(name="Group", slug="group")
        self.course = Course.objects.create(name="Course", slug="course", group=self.library_group)

        self.materials = []
        for index in range(3):
            textbook = Textbook.objects.create(name=f"Book {index}", slug=f"book-{index}", group=self.library_group)
            self.materials.append(
                CourseMaterial.objects.create(course=self.course, textbook=textbook, position=index)
            )

        self.teacher = User.objects.create_superuser(
            username="teacher",
            email="teacher@test.com",
            password="password",
        )

    def login(self):
        reset_current_user()
        self.client.logout()
        self.client.login(username="teacher", password="password")

    def move(self, material, direction):
        return self.client.post(
            reverse("course-material-move", args=[str(material.id)]),
            {"direction": direction},
            format="json",
        )

    def positions(self):
        """Return material ids ordered by their stored position."""
        return list(
            CourseMaterial.objects.filter(course=self.course).order_by("position").values_list("id", flat=True)
        )

    def test_move_down_swaps_with_next(self):
        self.login()
        first, second, third = self.materials

        response = self.move(first, "down")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.positions(), [second.id, first.id, third.id])

    def test_move_up_swaps_with_previous(self):
        self.login()
        first, second, third = self.materials

        response = self.move(third, "up")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.positions(), [first.id, third.id, second.id])

    def test_move_up_at_top_is_a_noop(self):
        self.login()
        first, second, third = self.materials

        response = self.move(first, "up")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.positions(), [first.id, second.id, third.id])

    def test_move_down_at_bottom_is_a_noop(self):
        self.login()
        first, second, third = self.materials

        response = self.move(third, "down")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.positions(), [first.id, second.id, third.id])

    def test_invalid_direction_is_rejected(self):
        self.login()

        response = self.move(self.materials[0], "sideways")

        self.assertEqual(response.status_code, 400)
