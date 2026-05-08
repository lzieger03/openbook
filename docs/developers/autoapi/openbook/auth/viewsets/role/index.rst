openbook.auth.viewsets.role
===========================

.. py:module:: openbook.auth.viewsets.role


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.role.RoleSerializer
   openbook.auth.viewsets.role.RoleFilter
   openbook.auth.viewsets.role.RoleViewSet


Module Contents
---------------

.. py:class:: RoleSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.role.RoleSerializer
      :parts: 1


   .. py:attribute:: scope_type


   .. py:attribute:: permissions


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'scope_type', 'scope_uuid', 'slug', 'name', 'description', 'text_format', 'priority',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



   .. py:method:: validate(attributes)

      Check that only allowed permissions are assigned.



.. py:class:: RoleFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.scope.ScopeFilterMixin`, :py:obj:`openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.role.RoleFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: RoleViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.role.RoleViewSet
      :parts: 1


   A viewset that provides default `create()`, `retrieve()`, `update()`,
   `partial_update()`, `destroy()` and `list()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'slug']



   .. py:attribute:: search_fields
      :value: ['slug', 'name', 'description']



