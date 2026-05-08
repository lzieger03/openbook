openbook.auth.admin.allowed_role_permission
===========================================

.. py:module:: openbook.auth.admin.allowed_role_permission


Classes
-------

.. autoapisummary::

   openbook.auth.admin.allowed_role_permission.AllowedRolePermissionResource
   openbook.auth.admin.allowed_role_permission.AllowedRolePermissionForm
   openbook.auth.admin.allowed_role_permission.AllowedRolePermissionAdmin


Module Contents
---------------

.. py:class:: AllowedRolePermissionResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.allowed_role_permission.AllowedRolePermissionResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: scope_type


   .. py:attribute:: permission


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'scope_type', 'permission']




.. py:class:: AllowedRolePermissionForm(*args, **kwargs)

   Bases: :py:obj:`django.forms.ModelForm`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.allowed_role_permission.AllowedRolePermissionForm
      :parts: 1


   The main implementation of all the Form logic. Note that this class is
   different than Form. See the comments by the Form class for more info. Any
   improvements to the form API should be made to this class, not to the Form
   class.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: '__all__'




   .. py:method:: clean()

      Check that only allowed scope types are assigned.



.. py:class:: AllowedRolePermissionAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.allowed_role_permission.AllowedRolePermissionAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['scope_type', 'perm_name', 'perm']



   .. py:attribute:: list_display_links
      :value: ['scope_type', 'perm_name', 'perm']



   .. py:attribute:: list_filter


   .. py:attribute:: search_fields
      :value: ['scope_type', 'permission__codename']



   .. py:attribute:: fieldsets


