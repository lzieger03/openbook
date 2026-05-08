openbook.auth.viewsets.permission
=================================

.. py:module:: openbook.auth.viewsets.permission


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.permission.PermissionSerializer
   openbook.auth.viewsets.permission.PermissionFilter
   openbook.auth.viewsets.permission.PermissionViewSet


Module Contents
---------------

.. py:class:: PermissionSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.permission.PermissionSerializer
      :parts: 1


   .. py:attribute:: perm_string


   .. py:attribute:: perm_display_name


   .. py:attribute:: app


   .. py:attribute:: app_display_name


   .. py:attribute:: model


   .. py:attribute:: model_display_name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'name', 'codename', 'perm_string', 'perm_display_name', 'app', 'app_display_name',...



      .. py:attribute:: read_only_fields
         :value: ['id']



      .. py:attribute:: expandable_fields



   .. py:method:: get_perm_string(obj)


   .. py:method:: get_perm_display_name(obj)


   .. py:method:: get_app(obj)


   .. py:method:: get_app_display_name(obj)


   .. py:method:: get_model(obj)


   .. py:method:: get_model_display_name(obj)


.. py:class:: PermissionFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.permission.PermissionFilter
      :parts: 1


   .. py:attribute:: perm_string


   .. py:attribute:: app


   .. py:attribute:: model


   .. py:attribute:: codename


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['app', 'model', 'codename']




   .. py:method:: filter_perm_string(queryset, name, value)


.. py:class:: PermissionViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.permission.PermissionViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: ordering
      :value: ['content_type__app_label', 'codename']



   .. py:attribute:: search_fields
      :value: ['content_type__app_label', 'codename']



