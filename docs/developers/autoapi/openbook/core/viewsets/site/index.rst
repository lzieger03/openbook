openbook.core.viewsets.site
===========================

.. py:module:: openbook.core.viewsets.site


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.site.SiteSerializer
   openbook.core.viewsets.site.SiteFilter
   openbook.core.viewsets.site.SiteViewSet


Module Contents
---------------

.. py:class:: SiteSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.site.SiteSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('id', 'domain', 'name', 'short_name', 'about_url', 'brand_color', 'auth_config')



      .. py:attribute:: expandable_fields



.. py:class:: SiteFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.site.SiteFilter
      :parts: 1


   .. py:attribute:: domain


   .. py:attribute:: name


   .. py:attribute:: short_name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('domain', 'name', 'short_name')




.. py:class:: SiteViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin`, :py:obj:`rest_framework.viewsets.ReadOnlyModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.site.SiteViewSet
      :parts: 1


   A viewset that provides default `list()` and `retrieve()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ('domain', 'short_name', 'name')



   .. py:attribute:: search_fields
      :value: ('domain', 'name', 'short_name')



   .. py:method:: health(request)

      Return a simple health status that the API is up and running.



