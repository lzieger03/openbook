openbook.content.admin.course
=============================

.. py:module:: openbook.content.admin.course


Classes
-------

.. autoapisummary::

   openbook.content.admin.course.CourseResource
   openbook.content.admin.course.CourseForm
   openbook.content.admin.course.CourseAdmin


Module Contents
---------------

.. py:class:: CourseResource(**kwargs)

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopedRolesResourceMixin`, :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.content.admin.course.CourseResource
      :parts: 1


   Mixin class for the import/export resource class of models that act as permissions
   scopes for user roles. Handles the import and export of the owner and public permissions.
   Note that the other scope fields (roles, enrollment methods, …) are not handled, because
   they are reverse relations for objects that support import/export themselves.


   .. py:attribute:: is_template


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'slug', 'name', 'description', 'text_format', 'owner', 'public_permissions',...




.. py:class:: CourseForm(*args, **kwargs)

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopedRolesFormMixin`

   .. autoapi-inheritance-diagram:: openbook.content.admin.course.CourseForm
      :parts: 1


   Form mixin for model forms where the model implements the `ScopedRoles` mixin and
   therefor acts as a permission scope for user roles. This mixin makes sure that
   only allowed permissions are assigned as public permissions.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: '__all__'




.. py:class:: CourseAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.content.admin.course.CourseAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['name', 'slug', 'is_template', 'owner', 'created_by', 'created_at', 'modified_by', 'modified_at']



   .. py:attribute:: list_display_links
      :value: ['name', 'slug', 'owner']



   .. py:attribute:: list_filter
      :value: ['name', 'is_template', 'owner', 'created_by', 'created_at', 'modified_by', 'modified_at']



   .. py:attribute:: list_select_related
      :value: ['created_by', 'modified_by']



   .. py:attribute:: search_fields
      :value: ['name', 'slug', 'owner', 'description']



   .. py:attribute:: ordering
      :value: ['name', 'slug']



   .. py:attribute:: readonly_fields
      :value: ['created_by', 'created_at', 'modified_by', 'modified_at']



   .. py:attribute:: prepopulated_fields


   .. py:attribute:: filter_horizontal
      :value: ['public_permissions']



   .. py:method:: get_inlines(request, obj)

      Hook for specifying custom inlines.



   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


