openbook.auth.viewsets.enrollment_method
========================================

.. py:module:: openbook.auth.viewsets.enrollment_method


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.enrollment_method.EnrollmentMethodSerializer
   openbook.auth.viewsets.enrollment_method.EnrollmentMethodFilter
   openbook.auth.viewsets.enrollment_method.EnrollmentMethodViewSet


Module Contents
---------------

.. py:class:: EnrollmentMethodSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.enrollment_method.EnrollmentMethodSerializer
      :parts: 1


   .. py:attribute:: scope_type


   .. py:attribute:: role


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'scope_type', 'scope_uuid', 'name', 'description', 'text_format', 'role', 'end_date',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



.. py:class:: EnrollmentMethodFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.scope.ScopeFilterMixin`, :py:obj:`openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.enrollment_method.EnrollmentMethodFilter
      :parts: 1


   .. py:attribute:: role


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



   .. py:method:: role_filter(queryset, name, value)


.. py:class:: EnrollmentMethodViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.enrollment_method.EnrollmentMethodViewSet
      :parts: 1


   A viewset that provides default `create()`, `retrieve()`, `update()`,
   `partial_update()`, `destroy()` and `list()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'name', 'role__slug']



   .. py:attribute:: search_fields
      :value: ['name', 'description', 'role__slug', 'role__name', 'role__description']



   .. py:method:: enroll(request, pk=None)

      Self-enrollment of the current user via given enrollment method.



