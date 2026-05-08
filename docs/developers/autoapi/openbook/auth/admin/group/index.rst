openbook.auth.admin.group
=========================

.. py:module:: openbook.auth.admin.group


Classes
-------

.. autoapisummary::

   openbook.auth.admin.group.GroupResource
   openbook.auth.admin.group.GroupAdmin


Module Contents
---------------

.. py:class:: GroupResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.group.GroupResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: permissions


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: import_id_fields
         :value: ['slug']



      .. py:attribute:: fields
         :value: ['slug', 'delete', 'name', 'permissions']




.. py:class:: GroupAdmin(model, admin_site)

   Bases: :py:obj:`django.contrib.auth.admin.GroupAdmin`, :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.group.GroupAdmin
      :parts: 1


   Sub-class of Django's Group Admin to allow importing and exporting groups.


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['name', 'slug', 'user_count']



   .. py:attribute:: list_display_links
      :value: ['name', 'slug']



   .. py:attribute:: prepopulated_fields


   .. py:attribute:: inlines


   .. py:attribute:: fieldsets


