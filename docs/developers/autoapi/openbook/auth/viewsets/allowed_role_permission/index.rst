openbook.auth.viewsets.allowed_role_permission
==============================================

.. py:module:: openbook.auth.viewsets.allowed_role_permission


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.allowed_role_permission.AllowedRolePermissionSerializer
   openbook.auth.viewsets.allowed_role_permission.AllowedRolePermissionFilter
   openbook.auth.viewsets.allowed_role_permission.AllowedRolePermissionViewSet


Module Contents
---------------

.. py:class:: AllowedRolePermissionSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.allowed_role_permission.AllowedRolePermissionSerializer
      :parts: 1


   .. py:attribute:: scope_type


   .. py:attribute:: permission


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'scope_type', 'permission']



      .. py:attribute:: expandable_fields



.. py:class:: AllowedRolePermissionFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.scope.ScopeTypeFilterMixin`, :py:obj:`openbook.auth.filters.mixins.permission.PermissionFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.allowed_role_permission.AllowedRolePermissionFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields


      .. py:attribute:: permissions_field
         :value: 'permission'




.. py:class:: AllowedRolePermissionViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.allowed_role_permission.AllowedRolePermissionViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['scope_type__app_label', 'scope_type__model', 'permission__content_type__app_label',...



   .. py:attribute:: search_fields
      :value: ['scope_type__app_label', 'scope_type__model', 'permission__content_type__app_label',...



