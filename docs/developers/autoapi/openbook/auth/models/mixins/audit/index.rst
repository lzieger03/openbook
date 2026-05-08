openbook.auth.models.mixins.audit
=================================

.. py:module:: openbook.auth.models.mixins.audit


Classes
-------

.. autoapisummary::

   openbook.auth.models.mixins.audit.CreatedModifiedByMixin


Module Contents
---------------

.. py:class:: CreatedModifiedByMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.auth.models.mixins.audit.CreatedModifiedByMixin
      :parts: 1


   Mixin class for models that shall record the time and user of creation as well as
   the time and user of the last modification.


   .. py:attribute:: created_by


   .. py:attribute:: created_at


   .. py:attribute:: modified_by


   .. py:attribute:: modified_at


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: save(*args, **kwargs)

      Automatically populate the `created_by` and `modified_by` fields.
      Care must be taken to call `super().save(*args, **kwargs)` when this method is overridden.



   .. py:property:: created_modified_by

      Get formatted string to display in the Admin or on the website.


