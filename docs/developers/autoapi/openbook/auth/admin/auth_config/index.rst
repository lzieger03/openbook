openbook.auth.admin.auth_config
===============================

.. py:module:: openbook.auth.admin.auth_config


Classes
-------

.. autoapisummary::

   openbook.auth.admin.auth_config.AuthConfigResource
   openbook.auth.admin.auth_config.AuthConfigTextResource
   openbook.auth.admin.auth_config.AuthConfigAdmin


Module Contents
---------------

.. py:class:: AuthConfigResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.auth_config.AuthConfigResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: site


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['site', 'delete', 'local_signup_allowed', 'signup_email_suffix', 'logout_next_url',...



      .. py:attribute:: import_id_fields
         :value: ['site']




   .. py:method:: get_display_name()
      :classmethod:



.. py:class:: AuthConfigTextResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.auth_config.AuthConfigTextResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: parent


   .. py:attribute:: language


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'parent', 'language', 'logout_next_text']




   .. py:method:: get_display_name()
      :classmethod:



   .. py:method:: filter_export(queryset, **kwargs)

      Needed because by default it is not possible to export another model than the one
      from the admin view.



.. py:class:: AuthConfigAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.auth_config.AuthConfigAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: ordering
      :value: ['site__domain']



   .. py:attribute:: list_display
      :value: ['site__domain', 'site__name', 'local_signup_allowed', 'signup_email_suffix', 'logout_next_url']



   .. py:attribute:: list_display_links
      :value: ['site__domain', 'site__name', 'local_signup_allowed', 'signup_email_suffix']



   .. py:attribute:: list_editable
      :value: ['logout_next_url']



   .. py:attribute:: list_select_related
      :value: ['site']



   .. py:attribute:: search_fields
      :value: ['site__domain', 'site__name', 'site__short_namesignup_email_suffix', 'logout_next_url']



   .. py:attribute:: inlines


   .. py:attribute:: fieldsets


