openbook.auth.admin.role_assignment
===================================

.. py:module:: openbook.auth.admin.role_assignment


Classes
-------

.. autoapisummary::

   openbook.auth.admin.role_assignment.RoleAssignmentResource
   openbook.auth.admin.role_assignment.RoleAssignmentForm
   openbook.auth.admin.role_assignment.RoleAssignmentInline
   openbook.auth.admin.role_assignment.RoleAssignmentAdmin


Module Contents
---------------

.. py:class:: RoleAssignmentResource

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeResourceMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role_assignment.RoleAssignmentResource
      :parts: 1


   .. py:attribute:: user


   .. py:attribute:: role


   .. py:attribute:: is_active


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: RoleAssignmentForm

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeFormMixin`, :py:obj:`openbook.auth.admin.mixins.scope.ScopeRoleFieldFormMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role_assignment.RoleAssignmentForm
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: '__all__'




   .. py:class:: Media

      .. py:attribute:: css


      .. py:attribute:: js



.. py:class:: RoleAssignmentInline(parent_model, admin_site)

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeRoleFieldInlineMixin`, :py:obj:`django.contrib.contenttypes.admin.GenericTabularInline`, :py:obj:`unfold.admin.TabularInline`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role_assignment.RoleAssignmentInline
      :parts: 1


   Options for inline editing of ``model`` instances.

   Provide ``fk_name`` to specify the attribute name of the ``ForeignKey``
   from ``model`` to its parent. This is required if ``model`` has more than
   one ``ForeignKey`` to its parent.


   .. py:attribute:: model


   .. py:attribute:: ct_field
      :value: 'scope_type'



   .. py:attribute:: ct_fk_field
      :value: 'scope_uuid'



   .. py:attribute:: fields
      :value: ['role', 'user', 'is_active', 'assignment_method', 'enrollment_method', 'access_request']



   .. py:attribute:: ordering
      :value: ['role', 'user']



   .. py:attribute:: readonly_fields
      :value: ['assignment_method', 'enrollment_method', 'access_request']



   .. py:attribute:: extra
      :value: 0



   .. py:attribute:: show_change_link
      :value: True



   .. py:attribute:: tab
      :value: True



.. py:class:: RoleAssignmentAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role_assignment.RoleAssignmentAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display


   .. py:attribute:: list_display_links
      :value: ['scope_type', 'scope_object', 'role', 'user', 'assignment_method']



   .. py:attribute:: list_select_related


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'role', 'user']



   .. py:attribute:: search_fields
      :value: ['role__name', 'user__username', 'user__first_name', 'user__last_name']



   .. py:attribute:: readonly_fields


   .. py:attribute:: list_filter


   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


