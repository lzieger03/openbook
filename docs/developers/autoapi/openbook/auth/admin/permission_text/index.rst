openbook.auth.admin.permission_text
===================================

.. py:module:: openbook.auth.admin.permission_text


Classes
-------

.. autoapisummary::

   openbook.auth.admin.permission_text.PermissionTextResource
   openbook.auth.admin.permission_text.PermissionTextAdmin


Module Contents
---------------

.. py:class:: PermissionTextResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.permission_text.PermissionTextResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: parent


   .. py:attribute:: language


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'parent', 'language', 'name']




.. py:class:: PermissionTextAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.permission_text.PermissionTextAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['appname', 'perm_name', 'perm', 'language', 'name']



   .. py:attribute:: list_display_links
      :value: ['appname', 'perm_name', 'perm', 'language']



   .. py:attribute:: list_editable
      :value: ['name']



   .. py:attribute:: search_fields
      :value: ['appname', 'perm_name', 'perm', 'language', 'name']



   .. py:attribute:: readonly_fields
      :value: ['appname', 'perm_name', 'perm']



   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


