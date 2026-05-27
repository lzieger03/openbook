# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.utils.translation import gettext_lazy as _

from openbook.core.models.mixins.uuid import UUIDMixin


class QuizQuestion(UUIDMixin):
    """
    A single quiz question with four choices and one designated correct choice.
    """

    class CorrectChoiceChoices(models.TextChoices):
        A = "A", _("Choice A")
        B = "B", _("Choice B")
        C = "C", _("Choice C")
        D = "D", _("Choice D")

    question_text = models.TextField(verbose_name=_("Question Text"))

    choice_a = models.CharField(verbose_name=_("Choice A"), max_length=255)

    choice_b = models.CharField(verbose_name=_("Choice B"), max_length=255)

    choice_c = models.CharField(verbose_name=_("Choice C"), max_length=255)

    choice_d = models.CharField(verbose_name=_("Choice D"), max_length=255)

    correct_choice = models.CharField(
        verbose_name=_("Correct Choice"),
        max_length=1,
        choices=CorrectChoiceChoices,
        default=CorrectChoiceChoices.A,
    )

    class Meta:
        verbose_name = _("Quiz Question")
        verbose_name_plural = _("Quiz Questions")
        ordering = ("question_text",)

    def __str__(self):
        return self.question_text[:50]
