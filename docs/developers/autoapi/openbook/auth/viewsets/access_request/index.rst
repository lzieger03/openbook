openbook.auth.viewsets.access_request
=====================================

.. py:module:: openbook.auth.viewsets.access_request


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.access_request.AccessRequestSerializer
   openbook.auth.viewsets.access_request.AccessRequestFilter
   openbook.auth.viewsets.access_request.AccessRequestViewSet


Module Contents
---------------

.. py:class:: AccessRequestSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.access_request.AccessRequestSerializer
      :parts: 1


   .. py:attribute:: scope_type


   .. py:attribute:: user


   .. py:attribute:: role


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'scope_type', 'scope_uuid', 'user', 'role', 'end_date', 'duration_period',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'decision_date', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



.. py:class:: AccessRequestFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.scope.ScopeFilterMixin`, :py:obj:`openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.access_request.AccessRequestFilter
      :parts: 1


   .. py:attribute:: role


   .. py:attribute:: user


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



   .. py:method:: role_filter(queryset, name, value)


   .. py:method:: user_filter(queryset, name, value)


.. py:class:: AccessRequestViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.access_request.AccessRequestViewSet
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



   .. py:method:: accept(request, pk)

      Accept request.



   .. py:method:: deny(request, pk)

      Deny request.



