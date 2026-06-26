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

from django.db import migrations

# Creating a course requires choosing (or creating) a library group, so teachers need
# to be able to create and manage library groups - not just courses. The Teacher group
# fixture only granted "add_course", which made the "create new library group" step of
# course creation fail. This mirrors the updated openbook_auth/groups fixture for fresh
# installs and backfills the permissions on existing databases.
TEACHER_LIBRARY_GROUP_PERMISSIONS = [
    ("openbook_content", "librarygroup", "add_librarygroup"),
    ("openbook_content", "librarygroup", "change_librarygroup"),
    ("openbook_content", "librarygroup", "view_librarygroup"),
]

TEACHER_GROUP_NAME = "Teacher"


def add_teacher_permissions(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission  = apps.get_model("auth", "Permission")
    Group       = apps.get_model("auth", "Group")

    teacher = Group.objects.filter(name=TEACHER_GROUP_NAME).first()

    if teacher is None:
        # On a brand-new database the Teacher group is created later by the
        # openbook_auth/groups fixture (via load_initial_data), which already carries
        # these permissions. Nothing to backfill here.
        return

    for app_label, model, codename in TEACHER_LIBRARY_GROUP_PERMISSIONS:
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            continue

        permission = Permission.objects.filter(content_type=content_type, codename=codename).first()

        if permission is None:
            continue

        teacher.permissions.add(permission)


def remove_teacher_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    Group      = apps.get_model("auth", "Group")

    teacher = Group.objects.filter(name=TEACHER_GROUP_NAME).first()

    if teacher is None:
        return

    codenames = [codename for _, _, codename in TEACHER_LIBRARY_GROUP_PERMISSIONS]
    permissions = Permission.objects.filter(
        content_type__app_label="openbook_content",
        codename__in=codenames,
    )
    teacher.permissions.remove(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("openbook_content", "0009_textbookpage_skills"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(add_teacher_permissions, remove_teacher_permissions),
    ]
