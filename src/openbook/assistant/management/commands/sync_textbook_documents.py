# OpenBook: Interactive Online Textbooks - Server
# Copyright 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.management.base import BaseCommand

from openbook.assistant.services.textbook_sync import TextbookDocumentSyncService
from openbook.content.models import Course
from openbook.content.models import CourseMaterial
from openbook.content.models import Textbook


class Command(BaseCommand):
    help = "Rebuild generated assistant documents from current textbook pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--course",
            help="UUID des Kurses, dessen Textbook-Dokumente neu erzeugt werden sollen.",
        )
        parser.add_argument(
            "--textbook",
            help="UUID des Textbooks, dessen kursbezogene Dokumente neu erzeugt werden sollen.",
        )

    def handle(self, *args, **options):
        materials = CourseMaterial.objects.select_related("course", "textbook").filter(
            textbook__isnull=False,
        )

        if options.get("course"):
            course = Course.objects.get(pk=options["course"])
            materials = materials.filter(course=course)

        if options.get("textbook"):
            textbook = Textbook.objects.get(pk=options["textbook"])
            materials = materials.filter(textbook=textbook)

        service = TextbookDocumentSyncService()
        synced_count = 0
        skipped_count = 0
        seen_pairs = set()

        for material in materials.order_by("course_id", "textbook_id"):
            pair = (material.course_id, material.textbook_id)
            if pair in seen_pairs:
                continue

            seen_pairs.add(pair)
            document = service.sync_textbook_for_course(
                textbook=material.textbook,
                course=material.course,
            )

            if document is None:
                skipped_count += 1
            else:
                synced_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Textbook documents rebuilt: "
                f"{synced_count}; skipped/deleted without page content: {skipped_count}."
            )
        )
