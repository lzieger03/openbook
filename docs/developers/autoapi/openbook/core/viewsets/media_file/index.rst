openbook.core.viewsets.media_file
=================================

.. py:module:: openbook.core.viewsets.media_file


Classes
-------

.. autoapisummary::

   openbook.core.viewsets.media_file.MediaFileSerializer
   openbook.core.viewsets.media_file.MediaFileFilter
   openbook.core.viewsets.media_file.MediaFileViewSet


Module Contents
---------------

.. py:class:: MediaFileSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.media_file.MediaFileSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('content_type', 'object_id', 'file_name', 'file_size', 'mime_type', 'file_data')



      .. py:attribute:: expandable_fields



.. py:class:: MediaFileFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.media_file.MediaFileFilter
      :parts: 1


   .. py:attribute:: file_name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('content_type', 'object_id', 'file_name', 'file_size', 'mime_type')




.. py:class:: MediaFileViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.core.viewsets.media_file.MediaFileViewSet
      :parts: 1


   A viewset that provides default `create()`, `retrieve()`, `update()`,
   `partial_update()`, `destroy()` and `list()` actions.


   .. py:attribute:: queryset


   .. py:attribute:: serializer_class


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ('content_type', 'object_id', 'file_name', 'file_size')



   .. py:attribute:: search_fields
      :value: ('file_name', 'mime_type')



