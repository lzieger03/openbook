# OpenBook: Interactive Online Textbooks
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class APISchemaTestCase(TestCase):
    def test_get_schema(self):
        """
        Don't crash when downloading the API schema.
        """
        response = self.client.get(reverse("api-schema"))
        self.assertEqual(response.status_code, 200)

    def test_asyncapi_docs_url_is_available(self):
        """
        Don't break the admin dropdown WebSocket API link.
        """
        self.assertEqual(reverse("asyncapi_docs"), "/ws/docs/")


class AdminSiteDropdownTestCase(TestCase):
    def test_site_dropdown_links_are_resolvable(self):
        """
        Don't crash the admin index while rendering dropdown links.
        """
        for item in settings.UNFOLD["SITE_DROPDOWN"]:
            str(item["link"])
