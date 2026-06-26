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

# A teacher needs more than "add_course" to actually run a course: they author the
# textbooks and pages, organise course materials, tag pages with skills (creating new
# ones on demand) and enrol students. The plain content/skill models and the
# course-scoped role models are all gated by model-level permissions (the auth backend
# falls back to them), so the Teacher group needs the full authoring set below. This
# mirrors the updated openbook_auth/groups fixture for fresh installs and backfills the
# permissions on existing databases.
TEACHER_AUTHORING_PERMISSIONS = [
    # Manage courses (creation already granted via "add_course").
    ("openbook_content", "course", "change_course"),
    ("openbook_content", "course", "delete_course"),
    ("openbook_content", "course", "view_course"),
    # Textbooks and their pages.
    ("openbook_content", "textbook", "add_textbook"),
    ("openbook_content", "textbook", "change_textbook"),
    ("openbook_content", "textbook", "delete_textbook"),
    ("openbook_content", "textbook", "view_textbook"),
    ("openbook_content", "textbookpage", "add_textbookpage"),
    ("openbook_content", "textbookpage", "change_textbookpage"),
    ("openbook_content", "textbookpage", "delete_textbookpage"),
    ("openbook_content", "textbookpage", "view_textbookpage"),
    # Course materials and their page ranges (the syllabus).
    ("openbook_content", "coursematerial", "add_coursematerial"),
    ("openbook_content", "coursematerial", "change_coursematerial"),
    ("openbook_content", "coursematerial", "delete_coursematerial"),
    ("openbook_content", "coursematerial", "view_coursematerial"),
    ("openbook_content", "coursematerialpagerange", "add_coursematerialpagerange"),
    ("openbook_content", "coursematerialpagerange", "change_coursematerialpagerange"),
    ("openbook_content", "coursematerialpagerange", "delete_coursematerialpagerange"),
    ("openbook_content", "coursematerialpagerange", "view_coursematerialpagerange"),
    # Student enrolment is modelled as a course-scoped student role + role assignments.
    ("openbook_auth", "role", "add_role"),
    ("openbook_auth", "role", "view_role"),
    ("openbook_auth", "roleassignment", "add_roleassignment"),
    ("openbook_auth", "roleassignment", "delete_roleassignment"),
    ("openbook_auth", "roleassignment", "view_roleassignment"),
    # Skills trained by pages (teachers may create new skills while tagging).
    ("openbook_gamification", "skill", "add_skill"),
    ("openbook_gamification", "skill", "view_skill"),
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

    for app_label, model, codename in TEACHER_AUTHORING_PERMISSIONS:
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

    for app_label, _model, codename in TEACHER_AUTHORING_PERMISSIONS:
        permission = Permission.objects.filter(
            content_type__app_label=app_label,
            codename=codename,
        ).first()
        if permission is not None:
            teacher.permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("openbook_content", "0010_teacher_librarygroup_permissions"),
        ("openbook_auth", "0003_signupgroupassignment_is_staff"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(add_teacher_permissions, remove_teacher_permissions),
    ]
