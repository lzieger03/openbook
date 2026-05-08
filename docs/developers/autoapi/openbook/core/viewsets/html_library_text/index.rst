openbook.core.viewsets.html_library_text
========================================

.. py:module:: openbook.core.viewsets.html_library_text


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.html_library_text.HTMLLibraryTextSerializer
   openbook.core.viewsets.html_library_text.HTMLLibraryTextFilter
   openbook.core.viewsets.html_library_text.HTMLLibraryTextViewSet


Module Contents
---------------

.. py:class:: HTMLLibraryTextSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library_text.HTMLLibraryTextSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'parent', 'language', 'short_description']



      .. py:attribute:: read_only_fields
         :value: ['id']



      .. py:attribute:: expandable_fields



.. py:class:: HTMLLibraryTextFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library_text.HTMLLibraryTextFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: HTMLLibraryTextViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_library_text.HTMLLibraryTextViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['parent__organization', 'parent__name', 'language']



   .. py:attribute:: search_fields
      :value: ['parent__organization', 'parent__name', 'short_description']



