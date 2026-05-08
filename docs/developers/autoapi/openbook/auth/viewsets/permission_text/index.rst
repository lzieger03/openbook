openbook.auth.viewsets.permission_text
======================================

.. py:module:: openbook.auth.viewsets.permission_text


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.permission_text.PermissionTextSerializer
   openbook.auth.viewsets.permission_text.PermissionTextFilter
   openbook.auth.viewsets.permission_text.PermissionTextViewSet


Module Contents
---------------

.. py:class:: PermissionTextSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.permission_text.PermissionTextSerializer
      :parts: 1


   .. py:attribute:: parent


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('id', 'language', 'parent', 'name')



      .. py:attribute:: expandable_fields



.. py:class:: PermissionTextFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.permission_text.PermissionTextFilter
      :parts: 1


   .. py:attribute:: perm_string


   .. py:attribute:: app


   .. py:attribute:: model


   .. py:attribute:: codename


   .. py:attribute:: name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['app', 'model', 'codename', 'language', 'name']




   .. py:method:: filter_perm_string(queryset, name, value)


.. py:class:: PermissionTextViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.permission_text.PermissionTextViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: ordering
      :value: ['parent__content_type__app_label', 'parent__codename', 'language__language']



   .. py:attribute:: search_fields
      :value: ['parent__content_type__app_label', 'parent__codename', 'language__language', 'language__name', 'name']



