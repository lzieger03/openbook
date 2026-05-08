openbook.auth.viewsets.role_assignment
======================================

.. py:module:: openbook.auth.viewsets.role_assignment


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.role_assignment.RoleAssignmentSerializer
   openbook.auth.viewsets.role_assignment.RoleAssignmentFilter
   openbook.auth.viewsets.role_assignment.RoleAssignmentViewSet


Module Contents
---------------

.. py:class:: RoleAssignmentSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.role_assignment.RoleAssignmentSerializer
      :parts: 1


   .. py:attribute:: scope_type


   .. py:attribute:: user


   .. py:attribute:: role


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'scope_type', 'scope_uuid', 'role', 'user', 'assignment_method', 'enrollment_method',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



.. py:class:: RoleAssignmentFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.scope.ScopeFilterMixin`, :py:obj:`openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.role_assignment.RoleAssignmentFilter
      :parts: 1


   .. py:attribute:: role


   .. py:attribute:: user


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



   .. py:method:: role_filter(queryset, name, value)


   .. py:method:: user_filter(queryset, name, value)


.. py:class:: RoleAssignmentViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.role_assignment.RoleAssignmentViewSet
      :parts: 1


   A viewset that provides default `create()`, `retrieve()`, `update()`,
   `partial_update()`, `destroy()` and `list()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'user__username', 'role__slug']



   .. py:attribute:: search_fields
      :value: ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'role__slug',...



