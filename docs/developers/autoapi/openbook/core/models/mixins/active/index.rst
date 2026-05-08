openbook.core.models.mixins.active
==================================

.. py:module:: openbook.core.models.mixins.active


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.active.ActiveInactiveMixin


Module Contents
---------------

.. py:class:: ActiveInactiveMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.active.ActiveInactiveMixin
      :parts: 1


   Mixin for models with an active/inactive state.

   The `__str__()` method returns `"(inactive)"`, if the object is inactive. This can be
   used in one's own `__str__()` implementation, if desired.


   .. py:attribute:: is_active


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




