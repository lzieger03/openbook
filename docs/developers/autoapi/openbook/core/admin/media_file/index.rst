openbook.core.admin.media_file
==============================

.. py:module:: openbook.core.admin.media_file


Classes
-------

.. autoapisummary::

   openbook.core.admin.media_file.MediaFileInline
   openbook.core.admin.media_file.MediaFileResource
   openbook.core.admin.media_file.MediaFileAdmin


Module Contents
---------------

.. py:class:: MediaFileInline(parent_model, admin_site)

   Bases: :py:obj:`django.contrib.contenttypes.admin.GenericTabularInline`

   .. autoapi-inheritance-diagram:: openbook.core.admin.media_file.MediaFileInline
      :parts: 1


   Options for inline editing of ``model`` instances.

   Provide ``fk_name`` to specify the attribute name of the ``ForeignKey``
   from ``model`` to its parent. This is required if ``model`` has more than
   one ``ForeignKey`` to its parent.


   .. py:attribute:: model


   .. py:attribute:: fields
      :value: ['file_data', 'file_name', 'file_size', 'mime_type']



   .. py:attribute:: readonly_fields
      :value: ['file_size', 'mime_type']



   .. py:attribute:: ordering
      :value: ['file_name']



   .. py:attribute:: extra
      :value: 0



   .. py:attribute:: show_change_link
      :value: True



   .. py:attribute:: tab
      :value: True



.. py:class:: MediaFileResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.media_file.MediaFileResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: content_type


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'content_type', 'object_id', 'file_data', 'file_name', 'file_size', 'mime_type']




.. py:class:: MediaFileAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.core.admin.media_file.MediaFileAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['content_type', 'object_id', 'file_name', 'file_size', 'mime_type', 'created_by', 'created_at',...



   .. py:attribute:: list_display_links
      :value: ['content_type', 'object_id', 'file_name', 'file_size', 'mime_type']



   .. py:attribute:: list_filter


   .. py:attribute:: list_select_related
      :value: ['created_by', 'modified_by']



   .. py:attribute:: readonly_fields
      :value: ['file_name', 'file_size', 'mime_type', 'created_by', 'created_at', 'modified_by', 'modified_at']



   .. py:attribute:: search_fields
      :value: ['file_name']



   .. py:attribute:: ordering
      :value: ['content_type', 'object_id', 'file_name']



   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


