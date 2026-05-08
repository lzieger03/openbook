openbook.auth.models.permission_text
====================================

.. py:module:: openbook.auth.models.permission_text


Classes
-------

.. autoapisummary::

   openbook.auth.models.permission_text.PermissionText


Module Contents
---------------

.. py:class:: PermissionText

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.i18n.TranslatableMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.permission_text.PermissionText
      :parts: 1


   Translated permission name.


   .. py:attribute:: parent


   .. py:attribute:: name


   .. py:class:: Meta

      Bases: :py:obj:`openbook.core.models.mixins.i18n.TranslatableMixin.Meta`

      .. autoapi-inheritance-diagram:: openbook.auth.models.permission_text.PermissionText.Meta
         :parts: 1


      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints



   .. py:method:: appname(obj=None)


   .. py:method:: perm_name(obj=None)


   .. py:method:: perm(obj=None)


