openbook.auth.filters.mixins.scope
==================================

.. py:module:: openbook.auth.filters.mixins.scope


Classes
-------

.. autoapisummary::

   openbook.auth.filters.mixins.scope.ScopedRolesFilterMixin
   openbook.auth.filters.mixins.scope.ScopeTypeFilterMixin
   openbook.auth.filters.mixins.scope.ScopeFilterMixin


Module Contents
---------------

.. py:class:: ScopedRolesFilterMixin

   Mixin filter class for any model that implements the `ScopedRolesMixin` and as such has
   an `owner` field.


   .. py:attribute:: owner


   .. py:class:: Meta

      .. py:attribute:: fields



   .. py:method:: owner_filter(queryset, name, value)


.. py:class:: ScopeTypeFilterMixin

   Mixin filter class for any model that has a `scope_type` field.


   .. py:attribute:: scope_type


   .. py:class:: Meta

      .. py:attribute:: fields



   .. py:method:: scope_type_filter(queryset, name, value)


.. py:class:: ScopeFilterMixin

   Bases: :py:obj:`ScopeTypeFilterMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.filters.mixins.scope.ScopeFilterMixin
      :parts: 1


   Mixin filter class for any model that implements the `ScopedMixin` and therefor has
   a `scope_type` and `scope_uuid` field.


   .. py:class:: Meta

      .. py:attribute:: fields



