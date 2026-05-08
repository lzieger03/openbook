openbook.core.viewsets.html_library_version
===========================================

.. py:module:: openbook.core.viewsets.html_library_version


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.html_library_version.HTMLLibraryVersionSerializer
   openbook.core.viewsets.html_library_version.HTMLLibraryVersionFilter
   openbook.core.viewsets.html_library_version.HTMLLibraryVersionViewSet


Module Contents
---------------

.. py:class:: HTMLLibraryVersionSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library_version.HTMLLibraryVersionSerializer
      :parts: 1


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'parent', 'version', 'dependencies', 'frontend_url', 'file_data', 'file_name',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'components', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



.. py:class:: HTMLLibraryVersionFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library_version.HTMLLibraryVersionFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: HTMLLibraryVersionViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library_version.HTMLLibraryVersionViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['parent__organization', 'parent__name', 'version']



   .. py:attribute:: search_fields
      :value: ['parent__organization', 'parent__name', 'version', 'dependencies']



