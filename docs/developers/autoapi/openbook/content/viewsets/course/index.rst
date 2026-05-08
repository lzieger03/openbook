openbook.content.viewsets.course
================================

.. py:module:: openbook.content.viewsets.course


Classes
-------

.. autoapisummary::

   openbook.content.viewsets.course.CourseSerializer
   openbook.content.viewsets.course.CourseFilter
   openbook.content.viewsets.course.CourseViewSet


Module Contents
---------------

.. py:class:: CourseSerializer(*args, **kwargs)

   Bases: :py:obj:`openbook.auth.serializers.mixins.scope.ScopedRolesSerializerMixin`, :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.content.viewsets.course.CourseSerializer
      :parts: 1


   Mixin class for model serializers whose models implement the `ScopedRolesMixin` and as such
   act as permission scope for user roles. Default serializer, that adds all scope fields.


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'slug', 'name', 'description', 'text_format', 'is_template', 'owner',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'role_assignments', 'enrollment_methods', 'access_requests', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



.. py:class:: CourseFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin`, :py:obj:`openbook.auth.filters.mixins.scope.ScopedRolesFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.content.viewsets.course.CourseFilter
      :parts: 1


   Mixin filter class for any model that implements the `CreatedModifiedByMixin` and has the
   `created_by`, `created_at`, `modified_by` and `modified_at` fields.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: CourseViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.content.viewsets.course.CourseViewSet
      :parts: 1


   A viewset that provides default `create()`, `retrieve()`, `update()`,
   `partial_update()`, `destroy()` and `list()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: search_fields
      :value: ['slug', 'name', 'description']



