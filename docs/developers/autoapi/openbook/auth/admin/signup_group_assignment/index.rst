openbook.auth.admin.signup_group_assignment
===========================================

.. py:module:: openbook.auth.admin.signup_group_assignment


Classes
-------

.. autoapisummary::

   openbook.auth.admin.signup_group_assignment.SignupGroupAssignmentResource
   openbook.auth.admin.signup_group_assignment.SecurityAssertionResource
   openbook.auth.admin.signup_group_assignment.SignupGroupAssignmentAdmin


Module Contents
---------------

.. py:class:: SignupGroupAssignmentResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.signup_group_assignment.SignupGroupAssignmentResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: site


   .. py:attribute:: groups


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'site', 'social_app', 'groups', 'name', 'description', 'text_format',...




   .. py:method:: get_display_name()
      :classmethod:



.. py:class:: SecurityAssertionResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.signup_group_assignment.SecurityAssertionResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'parent', 'name', 'value', 'match_strategy']




   .. py:method:: get_display_name()
      :classmethod:



   .. py:method:: filter_export(queryset, **kwargs)

      Needed because by default it is not possible to export another model than the one
      from the admin view.



.. py:class:: SignupGroupAssignmentAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.signup_group_assignment.SignupGroupAssignmentAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: ordering
      :value: ['name']



   .. py:attribute:: list_display
      :value: ['name', 'site__domain', 'site__name', 'social_app']



   .. py:attribute:: list_display_links
      :value: ['name', 'site__domain', 'site__name', 'social_app']



   .. py:attribute:: list_select_related
      :value: ['site', 'social_app']



   .. py:attribute:: search_fields
      :value: ['site__domain', 'site__name', 'site__short_name', 'social_app__name',...



   .. py:attribute:: filter_horizontal
      :value: ['groups']



   .. py:attribute:: inlines


   .. py:method:: get_queryset(request)

      Return a QuerySet of all model instances that can be edited by the
      admin site. This is used by changelist_view.



   .. py:attribute:: fieldsets


