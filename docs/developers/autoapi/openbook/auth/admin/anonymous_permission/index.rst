openbook.auth.admin.anonymous_permission
========================================

.. py:module:: openbook.auth.admin.anonymous_permission


Classes
-------

.. autoapisummary::

   openbook.auth.admin.anonymous_permission.AnonymousPermissionResource
   openbook.auth.admin.anonymous_permission.AnonymousPermissionAdmin


Module Contents
---------------

.. py:class:: AnonymousPermissionResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.anonymous_permission.AnonymousPermissionResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: permission


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'permission']




.. py:class:: AnonymousPermissionAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.anonymous_permission.AnonymousPermissionAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['perm_name', 'perm']



   .. py:attribute:: list_display_links
      :value: ['perm_name', 'perm']



   .. py:attribute:: list_filter


   .. py:attribute:: search_fields
      :value: ['permission__codename']



   .. py:attribute:: fieldsets


