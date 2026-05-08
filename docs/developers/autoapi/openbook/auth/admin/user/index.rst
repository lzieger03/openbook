openbook.auth.admin.user
========================

.. py:module:: openbook.auth.admin.user


Classes
-------

.. autoapisummary::

   openbook.auth.admin.user.UserResource
   openbook.auth.admin.user.UserAdmin


Module Contents
---------------

.. py:class:: UserResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.user.UserResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: is_active


   .. py:attribute:: is_staff


   .. py:attribute:: is_superuser


   .. py:attribute:: groups


   .. py:attribute:: user_permissions


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: import_id_fields
         :value: ['username']



      .. py:attribute:: fields
         :value: ['username', 'delete', 'user_type', 'email', 'first_name', 'last_name', 'date_joined',...




.. py:class:: UserAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`, :py:obj:`django.contrib.auth.admin.UserAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.user.UserAdmin
      :parts: 1


   Sub-class of Django's User Admin to integrate the additional fields of
   Application Users.


   .. py:attribute:: form


   .. py:attribute:: add_form


   .. py:attribute:: change_password_form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['full_name', 'username', 'is_staff', 'is_superuser', 'user_type']



   .. py:attribute:: list_display_links
      :value: ['full_name', 'username']



   .. py:attribute:: list_filter
      :value: ['is_staff', 'is_superuser', 'is_active', 'groups', 'is_superuser', 'user_type']



   .. py:attribute:: list_sections


   .. py:attribute:: inlines


   .. py:method:: get_queryset(request)

      Prefetch relations to optimize database performance for the changelist sections.



   .. py:attribute:: add_fieldsets


   .. py:method:: get_form(request, obj=None, **kwargs)

      Override e-mail to be obligatory.
      See: https://stackoverflow.com/a/66562177



