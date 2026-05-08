openbook.core.models.mixins.uuid
================================

.. py:module:: openbook.core.models.mixins.uuid


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.uuid.UUIDMixin


Module Contents
---------------

.. py:class:: UUIDMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.uuid.UUIDMixin
      :parts: 1


   Mixin for models with a UUID primary key instead of Django's default Auto ID
   integer sequence. Since we might often use the IDs in APIs and URLs, for security
   reasons, we want to avoid predictable sequences. But unfortunately we cannot
   enforce this in Django, as Auto IDs needs to be integers.


   .. py:attribute:: id


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: save(*args, **kwargs)

      Assign new UUID when saving a new entry.



