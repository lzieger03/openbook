openbook.auth.models.anonymous_permission
=========================================

.. py:module:: openbook.auth.models.anonymous_permission


Classes
-------

.. autoapisummary::

   openbook.auth.models.anonymous_permission.AnonymousPermission


Module Contents
---------------

.. py:class:: AnonymousPermission

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.anonymous_permission.AnonymousPermission
      :parts: 1


   Permissions for anonymous (not logged-in) users. Required for our implementation of
   object-based permissions which by default fail for anonymous users. Note, that these
   permissions are automatically valid for authenticated users, too.


   .. py:attribute:: permission


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints



   .. py:method:: perm_name(obj=None)


   .. py:method:: perm(obj=None)


