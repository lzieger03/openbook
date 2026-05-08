openbook.core.viewsets.language
===============================

.. py:module:: openbook.core.viewsets.language


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.language.LanguageSerializer
   openbook.core.viewsets.language.LanguageFilter
   openbook.core.viewsets.language.LanguageViewSet


Module Contents
---------------

.. py:class:: LanguageSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.language.LanguageSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('language', 'name')



      .. py:attribute:: expandable_fields



.. py:class:: LanguageFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.language.LanguageFilter
      :parts: 1


   .. py:attribute:: name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('name',)




.. py:class:: LanguageViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.language.LanguageViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ('language',)



   .. py:attribute:: search_fields
      :value: ('language', 'name')



