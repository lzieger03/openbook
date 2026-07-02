# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)

from django.db import IntegrityError
from django.test import TestCase

from ..models import Skill


class Skill_Model_Tests(TestCase):
    """Tests for the Skill model."""

    def test_skill_defaults(self):
        """A new skill uses empty optional text fields by default."""
        skill = Skill.objects.create(name="Python")

        self.assertEqual(skill.description, "")
        self.assertEqual(skill.icon_path, "")

    def test_skill_name_is_unique(self):
        """Two skills cannot use the same name."""
        Skill.objects.create(name="Python")

        with self.assertRaises(IntegrityError):
            Skill.objects.create(name="Python")
