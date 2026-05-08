openbook.core.viewsets.html_component_definition
================================================

.. py:module:: openbook.core.viewsets.html_component_definition


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.html_component_definition.HTMLComponentDefinitionSerializer
   openbook.core.viewsets.html_component_definition.HTMLComponentDefinitionFilter
   openbook.core.viewsets.html_component_definition.HTMLComponentDefinitionViewSet


Module Contents
---------------

.. py:class:: HTMLComponentDefinitionSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_component_definition.HTMLComponentDefinitionSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'html_component', 'library_version', 'definition']



      .. py:attribute:: read_only_fields
         :value: ['id']



      .. py:attribute:: expandable_fields



.. py:class:: HTMLComponentDefinitionFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_component_definition.HTMLComponentDefinitionFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: HTMLComponentDefinitionViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.html_component_definition.HTMLComponentDefinitionViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['html_component__library__organization', 'html_component__library__name',...



   .. py:attribute:: search_fields
      :value: ['html_component__library__organization', 'html_component__library__name',...



