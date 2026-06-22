# OpenBook: Interactive Online Textbooks
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

import uuid

from django.db import migrations

# Course content authored in the teacher area must be readable by learners (and
# anonymous visitors) so it can be shown on the dashboard. Object-level view
# permissions are granted globally via AnonymousPermission, which - despite its
# name - also applies to authenticated users. This mirrors the entries in the
# openbook_auth/anonymous_permissions fixture for fresh installs; this migration
# backfills them on existing databases.
CONTENT_VIEW_PERMISSIONS = [
    ("openbook_content", "coursematerial",          "view_coursematerial"),
    ("openbook_content", "coursematerialpagerange", "view_coursematerialpagerange"),
    ("openbook_content", "textbookpage",            "view_textbookpage"),
]


def add_anonymous_permissions(apps, schema_editor):
    ContentType         = apps.get_model("contenttypes", "ContentType")
    Permission          = apps.get_model("auth", "Permission")
    AnonymousPermission = apps.get_model("openbook_auth", "AnonymousPermission")

    for app_label, model, codename in CONTENT_VIEW_PERMISSIONS:
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            # On a brand-new database the content types / permissions are created by
            # the post-migrate signal that runs after this migration. Such installs
            # receive the entries from the fixture via ``load_initial_data`` instead.
            continue

        permission = Permission.objects.filter(content_type=content_type, codename=codename).first()

        if permission is None:
            continue

        # The UUID primary key is normally assigned in the model's save() override,
        # which historical migration models do not have, so set it explicitly.
        AnonymousPermission.objects.get_or_create(
            permission=permission,
            defaults={"id": uuid.uuid4()},
        )


def remove_anonymous_permissions(apps, schema_editor):
    AnonymousPermission = apps.get_model("openbook_auth", "AnonymousPermission")
    codenames = [codename for _, _, codename in CONTENT_VIEW_PERMISSIONS]
    AnonymousPermission.objects.filter(permission__codename__in=codenames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("openbook_content", "0007_course_skills"),
        ("openbook_auth", "0003_signupgroupassignment_is_staff"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(add_anonymous_permissions, remove_anonymous_permissions),
    ]
