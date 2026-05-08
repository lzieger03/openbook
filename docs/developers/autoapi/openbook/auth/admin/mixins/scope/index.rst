openbook.auth.admin.mixins.scope
================================

.. py:module:: openbook.auth.admin.mixins.scope


Attributes
----------

.. autoapisummary::

   openbook.auth.admin.mixins.scope.scope_type_filter
   openbook.auth.admin.mixins.scope.permissions_fieldset


Classes
-------

.. autoapisummary::

   openbook.auth.admin.mixins.scope.ScopedRolesResourceMixin
   openbook.auth.admin.mixins.scope.ScopeResourceMixin
   openbook.auth.admin.mixins.scope.ScopeFormMixin
   openbook.auth.admin.mixins.scope.ScopeRoleFieldFormMixin
   openbook.auth.admin.mixins.scope.ScopeRoleFieldInlineMixin
   openbook.auth.admin.mixins.scope.ScopedRolesFormMixin


Module Contents
---------------

.. py:data:: scope_type_filter

.. py:data:: permissions_fieldset

.. py:class:: ScopedRolesResourceMixin(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.mixins.scope.ScopedRolesResourceMixin
      :parts: 1


   Mixin class for the import/export resource class of models that act as permissions
   scopes for user roles. Handles the import and export of the owner and public permissions.
   Note that the other scope fields (roles, enrollment methods, …) are not handled, because
   they are reverse relations for objects that support import/export themselves.


   .. py:attribute:: owner


   .. py:attribute:: public_permissions


   .. py:class:: Meta

      .. py:attribute:: fields
         :value: ['owner', 'public_permissions']




.. py:class:: ScopeResourceMixin(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.mixins.scope.ScopeResourceMixin
      :parts: 1


   Mixin class for the import/export resource class of models that reference an authorization
   scope with the fields `scope_type` and `scope_uuid`.


   .. py:attribute:: scope_type


   .. py:attribute:: scope_id


   .. py:class:: Meta

      .. py:attribute:: fields
         :value: ['scope_type', 'scope_id']




   .. py:method:: dehydrate_scope_id(instance)

      Export scope id using either slug (if existing as it should) or id of the scope model.



   .. py:method:: before_save_instance(instance, row, **kwargs)

      Resolve slug from scope model back to UUID.



.. py:class:: ScopeFormMixin(*args, **kwargs)

   Bases: :py:obj:`django.forms.ModelForm`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.mixins.scope.ScopeFormMixin
      :parts: 1


   Form mixin class for model forms where the model implements the `ScopeMixin`
   and therefor has two fields for scope type and scope uuid. The form mixin
   (this class) limits the list of scope types to valid choices and automatically
   updates the scope uuid list when the type is changed. Instead of the uuid the
   scope name will be shown in the select box.


   .. py:class:: Meta

      .. py:attribute:: fields
         :value: ('scope_uuid',)




   .. py:class:: Media

      .. py:attribute:: css


      .. py:attribute:: js
         :value: ['openbook_auth/scope_uuid_autoload.js']




   .. py:method:: clean()

      Check that only allowed scope types are assigned.



.. py:class:: ScopeRoleFieldFormMixin(data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None)

   Bases: :py:obj:`django.forms.ModelForm`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.mixins.scope.ScopeRoleFieldFormMixin
      :parts: 1


   Form mixin for the enrollment models that combine a scope with a role, e.g. User role
   assignment, enrollment method etc. This mixin makes sure that only active roles of
   the selected scope can be chosen and updates the role selection list accordingly
   when the scope is changed.


   .. py:class:: Media

      .. py:attribute:: css


      .. py:attribute:: js
         :value: ['openbook_auth/scope_roles_autoload.js']




.. py:class:: ScopeRoleFieldInlineMixin(model, admin_site)

   Bases: :py:obj:`unfold.admin.TabularInline`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.mixins.scope.ScopeRoleFieldInlineMixin
      :parts: 1


   Tabular inline mixin that restricts the choice of roles to the current scope.


   .. py:method:: get_formset(request, obj=None, **kwargs)

      Return a BaseInlineFormSet class for use in add/change views.



   .. py:method:: formfield_for_foreignkey(db_field, request, **kwargs)

      Get a form Field for a ForeignKey.



.. py:class:: ScopedRolesFormMixin(*args, **kwargs)

   Bases: :py:obj:`django.forms.ModelForm`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.mixins.scope.ScopedRolesFormMixin
      :parts: 1


   Form mixin for model forms where the model implements the `ScopedRoles` mixin and
   therefor acts as a permission scope for user roles. This mixin makes sure that
   only allowed permissions are assigned as public permissions.


   .. py:method:: clean()

      Check that only allowed permissions are assigned.



