openbook.auth.filters.mixins.permission
=======================================

.. py:module:: openbook.auth.filters.mixins.permission


Classes
-------

.. autoapisummary::

   openbook.auth.filters.mixins.permission.PermissionsFilterMixin
   openbook.auth.filters.mixins.permission.PermissionFilterMixin


Module Contents
---------------

.. py:class:: PermissionsFilterMixin

   Mixin filter class for any model that has a M2M relationship on the Django permission object.
   This allows to filter queries by the full permission string. Use it like this:

   ```python
   class RoleFilter(PermissionsFilterMixin, filters.FilterSet):
       class Meta:
           model  = Role
           fields = […] # Only fields from model allowed!
           permissions_field = "public_permissions" # If not called `permissions`
   ```

   This works hand in hand with the shared `PermissionSerializer` class.


   .. py:attribute:: permissions


   .. py:class:: Meta

      .. py:attribute:: fields



   .. py:method:: permissions_filter(queryset, name, value)


.. py:class:: PermissionFilterMixin

   Bases: :py:obj:`PermissionsFilterMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.filters.mixins.permission.PermissionFilterMixin
      :parts: 1


   Like `PermissionsFilterMixin` but for FK relationships to Django permissions


   .. py:attribute:: permission


   .. py:attribute:: permissions
      :value: None



   .. py:class:: Meta

      .. py:attribute:: fields


      .. py:attribute:: permissions_field
         :value: 'permission'




