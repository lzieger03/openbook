# OpenBook: Interactive Online Textbooks
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.core.exceptions        import ValidationError as DjangoValidationError
from rest_flex_fields2.serializers import FlexFieldsModelSerializer as RFFFlexFieldsModelSerializer
from rest_framework.exceptions     import ValidationError as DRFValidationError

class FlexFieldsModelSerializer(RFFFlexFieldsModelSerializer):
    """
    Reuse full cleaning and validation logic of the models in the REST API.

    Reuse ``full_clean()``, ``clean()``, field validation, and uniqueness checks.
    Also make sure that the pre-filled model instance can be accessed in the DRF view.
    """
    def validate(self, attrs):
        # Create or update instance for validation and cache for access in view
        self._instance = self.instance or self.Meta.model()

<<<<<<< HEAD
        for attr, value in attrs.items():
=======
        # Many-to-many fields cannot be assigned directly on an unsaved instance and are
        # not part of ``full_clean()``; DRF sets them via ``.set()`` after save. Skip them
        # here so pre-save validation works for models with m2m fields (e.g. permissions).
        m2m_field_names = {field.name for field in self._instance._meta.many_to_many}

        for attr, value in attrs.items():
            if attr in m2m_field_names:
                continue

>>>>>>> origin/frontend-ai-integration-test
            setattr(self._instance, attr, value)

        try:
            self._instance.full_clean()
        except DjangoValidationError as e:
            # Convert Django's ValidationError to DRF's ValidationError
            raise DRFValidationError(e.message_dict)

        return attrs

    def get_prefilled_instance(self):
        """
        Access the pre-filled model instance in ``ModelViewSetMixin``.
        """
        return getattr(self, '_instance', None)
