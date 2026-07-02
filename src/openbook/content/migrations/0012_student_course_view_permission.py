# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.db import migrations

# The AI assistant (chat, quizzes and exams) requires "view_course" on the course
# (orchestrator._check_chat_permission). Enrolment is recorded as a permission-less
# course role, so students had no way to satisfy that check and saw "You are not
# allowed to use the assistant for this course." Grant the Student group the
# view_course model permission. Mirrors the updated openbook_auth/groups fixture for
# fresh installs and backfills existing databases.
STUDENT_VIEW_PERMISSIONS = [
    ("openbook_content", "course", "view_course"),
]

STUDENT_GROUP_NAME = "Student"


def add_student_permissions(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission  = apps.get_model("auth", "Permission")
    Group       = apps.get_model("auth", "Group")

    student = Group.objects.filter(name=STUDENT_GROUP_NAME).first()

    if student is None:
        # On a brand-new database the Student group is created later by the
        # openbook_auth/groups fixture (via load_initial_data), which already carries
        # this permission. Nothing to backfill here.
        return

    for app_label, model, codename in STUDENT_VIEW_PERMISSIONS:
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            continue

        permission = Permission.objects.filter(content_type=content_type, codename=codename).first()

        if permission is None:
            continue

        student.permissions.add(permission)


def remove_student_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    Group      = apps.get_model("auth", "Group")

    student = Group.objects.filter(name=STUDENT_GROUP_NAME).first()

    if student is None:
        return

    for app_label, _model, codename in STUDENT_VIEW_PERMISSIONS:
        permission = Permission.objects.filter(
            content_type__app_label=app_label,
            codename=codename,
        ).first()
        if permission is not None:
            student.permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("openbook_content", "0011_teacher_authoring_permissions"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(add_student_permissions, remove_student_permissions),
    ]
