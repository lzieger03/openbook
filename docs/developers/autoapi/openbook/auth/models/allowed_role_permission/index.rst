openbook.auth.models.allowed_role_permission
============================================

.. py:module:: openbook.auth.models.allowed_role_permission


Classes
-------

.. autoapisummary::

   openbook.auth.models.allowed_role_permission.AllowedRolePermission


Module Contents
---------------

.. py:class:: AllowedRolePermission

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.allowed_role_permission.AllowedRolePermission
      :parts: 1


   Allowed permission to be used in scoped roles. This is used to restrict the list of available
   permissions when defining roles.


   .. py:attribute:: scope_type


   .. py:attribute:: permission


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: indexes


      .. py:attribute:: constraints



   .. py:method:: get_for_scope_type(scope_type)
      :classmethod:


      Get a list of allowed permissions for the given scope type.



   .. py:method:: perm_name(obj=None)


   .. py:method:: perm(obj=None)


