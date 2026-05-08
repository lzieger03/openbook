openbook.core.admin.html_library
================================

.. py:module:: openbook.core.admin.html_library


Classes
-------

.. autoapisummary::

   openbook.core.admin.html_library.HTMLLibraryResource
   openbook.core.admin.html_library.HTMLLibraryTextResource
   openbook.core.admin.html_library.HTMLLibraryVersionResource
   openbook.core.admin.html_library.HTMLLibraryAdmin


Module Contents
---------------

.. py:class:: HTMLLibraryResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_library.HTMLLibraryResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: published


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'organization', 'name', 'author', 'license', 'website', 'coderepo',...




   .. py:method:: get_display_name()
      :classmethod:



.. py:class:: HTMLLibraryTextResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_library.HTMLLibraryTextResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ('id', 'delete', 'parent', 'language', 'short_description')




   .. py:method:: get_display_name()
      :classmethod:



   .. py:method:: filter_export(queryset, **kwargs)

      Needed because by default it is not possible to export another model than the one
      from the admin view.



.. py:class:: HTMLLibraryVersionResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_library.HTMLLibraryVersionResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'parent', 'version', 'dependencies', 'frontend_url', 'file_data', 'file_name',...




   .. py:method:: get_display_name()
      :classmethod:



   .. py:method:: filter_export(queryset, **kwargs)

      Needed because by default it is not possible to export another model than the one
      from the admin view.



.. py:class:: HTMLLibraryAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_library.HTMLLibraryAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['fqn', 'author', 'license', 'published', 'created_by', 'created_at', 'modified_by', 'modified_at']



   .. py:attribute:: list_display_links
      :value: ['fqn', 'author', 'license', 'published']



   .. py:attribute:: list_filter


   .. py:attribute:: list_select_related
      :value: ['created_by', 'modified_by']



   .. py:attribute:: readonly_fields
      :value: ['fqn', 'created_by', 'created_at', 'modified_by', 'modified_at']



   .. py:attribute:: search_fields
      :value: ['organization', 'name', 'author']



   .. py:attribute:: ordering
      :value: ['organization', 'name']



   .. py:attribute:: list_sections


   .. py:attribute:: inlines


   .. py:attribute:: actions_list
      :value: []



   .. py:attribute:: actions_detail
      :value: ['unpack_archives']



   .. py:method:: get_queryset(request)

      Return a QuerySet of all model instances that can be edited by the
      admin site. This is used by changelist_view.



   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


   .. py:method:: unpack_archives(request, object_id)


