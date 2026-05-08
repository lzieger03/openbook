openbook.core.admin.html_component
==================================

.. py:module:: openbook.core.admin.html_component


Classes
-------

.. autoapisummary::

   openbook.core.admin.html_component.HTMLComponentResource
   openbook.core.admin.html_component.HTMLComponentDefinitionResource
   openbook.core.admin.html_component.HTMLComponentAdmin


Module Contents
---------------

.. py:class:: HTMLComponentResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_component.HTMLComponentResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: library


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'library', 'tag_name']




   .. py:method:: get_display_name()
      :classmethod:



.. py:class:: HTMLComponentDefinitionResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_component.HTMLComponentDefinitionResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: library


   .. py:attribute:: version


   .. py:attribute:: tag_name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'library', 'version', 'tag_name', 'definition']




   .. py:method:: import_field(field, instance, row, is_m2m=False, **kwargs)

      Handles persistence of the field data.

      :param field: A :class:`import_export.fields.Field` instance.

      :param instance: A new or existing model instance.

      :param row: A ``dict`` containing key / value data for the row to be imported.

      :param is_m2m: A boolean value indicating whether or not this is a
        many-to-many field.

      :param \**kwargs:
          See :meth:`import_row`



   .. py:method:: get_display_name()
      :classmethod:



.. py:class:: HTMLComponentAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.core.admin.html_component.HTMLComponentAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['library', 'tag_name', 'min_version', 'max_version']



   .. py:attribute:: list_display_links
      :value: ['library', 'tag_name', 'min_version', 'max_version']



   .. py:attribute:: list_filter
      :value: ['library__organization', 'library__author']



   .. py:attribute:: list_select_related
      :value: ['library']



   .. py:attribute:: readonly_fields
      :value: ['library_readonly', 'min_version', 'max_version']



   .. py:attribute:: search_fields
      :value: ['library__organization', 'library__name', 'library__author', 'tag_name']



   .. py:attribute:: ordering
      :value: ['library__organization', 'library__name', 'tag_name']



   .. py:attribute:: list_sections


   .. py:attribute:: inlines


   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


   .. py:method:: get_formsets_with_inlines(request, obj=None)

      Hide inlines in the add view, since first the model must be saved to know
      from which library the allowed versions come from.



   .. py:method:: library_readonly(obj)


