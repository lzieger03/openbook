openbook.auth.admin.auth_token
==============================

.. py:module:: openbook.auth.admin.auth_token


Classes
-------

.. autoapisummary::

   openbook.auth.admin.auth_token.AuthTokenResource
   openbook.auth.admin.auth_token.AuthTokenAdmin


Module Contents
---------------

.. py:class:: AuthTokenResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.auth_token.AuthTokenResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: user


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'user', 'token', 'name', 'description', 'text_format', 'is_active',...




.. py:class:: AuthTokenAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.auth_token.AuthTokenAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: ordering
      :value: ['user__username', 'token']



   .. py:attribute:: list_display


   .. py:attribute:: list_display_links
      :value: ['user__username', 'name', 'is_active', 'start_date', 'end_date']



   .. py:attribute:: list_filter


   .. py:attribute:: list_select_related


   .. py:attribute:: search_fields
      :value: ['user__username', 'token', 'namedescription']



   .. py:attribute:: readonly_fields


   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


