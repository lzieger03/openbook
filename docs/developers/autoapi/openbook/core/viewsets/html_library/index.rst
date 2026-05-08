openbook.core.viewsets.html_library
===================================

.. py:module:: openbook.core.viewsets.html_library


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.html_library.HTMLLibrarySerializer
   openbook.core.viewsets.html_library.HTMLLibraryFilter
   openbook.core.viewsets.html_library.HTMLLibraryViewSet


Module Contents
---------------

.. py:class:: HTMLLibrarySerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library.HTMLLibrarySerializer
      :parts: 1


   .. py:attribute:: fqn


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'fqn', 'organization', 'name', 'author', 'license', 'website', 'coderepo', 'bugtracker',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'fqn', 'translations', 'versions', 'components', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



   .. py:method:: get_fqn(obj)


.. py:class:: HTMLLibraryFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library.HTMLLibraryFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: HTMLLibraryViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library.HTMLLibraryViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['organization', 'name']



   .. py:attribute:: search_fields
      :value: ['organization', 'name', 'author', 'license']



