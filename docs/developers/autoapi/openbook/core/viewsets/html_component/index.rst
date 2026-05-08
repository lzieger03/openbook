openbook.core.viewsets.html_component
=====================================

.. py:module:: openbook.core.viewsets.html_component


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.html_component.HTMLComponentSerializer
   openbook.core.viewsets.html_component.HTMLComponentFilter
   openbook.core.viewsets.html_component.HTMLComponentViewSet


Module Contents
---------------

.. py:class:: HTMLComponentSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_component.HTMLComponentSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'library', 'tag_name', 'definitions']



      .. py:attribute:: read_only_fields
         :value: ['id', 'definitions']



      .. py:attribute:: expandable_fields



.. py:class:: HTMLComponentFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_component.HTMLComponentFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: HTMLComponentViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_component.HTMLComponentViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['library__organization', 'library__name', 'tag_name']



   .. py:attribute:: search_fields
      :value: ['library__organization', 'library__name', 'library__author', 'tag_name']



