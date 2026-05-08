openbook.auth.models.mixins.scope
=================================

.. py:module:: openbook.auth.models.mixins.scope


Classes
-------

.. autoapisummary::

   openbook.auth.models.mixins.scope.RoleBasedObjectPermissionsMixin
   openbook.auth.models.mixins.scope.ScopedRolesMixin
   openbook.auth.models.mixins.scope.ScopeMixin


Module Contents
---------------

.. py:class:: RoleBasedObjectPermissionsMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.auth.models.mixins.scope.RoleBasedObjectPermissionsMixin
      :parts: 1


   Mixin class for all models that support role-based object permissions. Use this instead of
   `ScopedRolesMixin` for composite models, where the model itself is not the scope for the roles,
   e.g. for course materials where the roles belong to the parent course. Override `get_scope()`
   to return the parent model, which must inherit `ScopedRolesMixin`, instead.


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: has_obj_perm(user_obj, perm)

      Check if the given user has the given permission on the object. This always checks the public
      permissions of the scope and all role assignments, if the user is authenticated. Unless the
      user is the owner of the scope in which case (s)he is always allowed.

      This method can be overridden to implement custom permission checks. Usually
      `super().has_obj_perm(user_obj, perm)` should still be called, then.

      Note, this method is called `has_obj_perm()` instead of `has_perm()` because the Django user model
      already has a method `has_perm()`.



   .. py:method:: get_scope()

      Get the model instance with the role assignments. Usually this is the object itself, but for
      composite models like course materials and courses this should be the parent object (e.g. course).
      In that case this method must be overridden to return the parent object.



.. py:class:: ScopedRolesMixin(*args, **kwargs)

   Bases: :py:obj:`RoleBasedObjectPermissionsMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.mixins.scope.ScopedRolesMixin
      :parts: 1


   Mixin class for models that have scoped roles to grant permissions. Inheriting this mixin allows
   the model to have roles, role assignment, enrollment methods and access requests. This includes the
   `RoleBasedObjectPermissionsMixin`, so that object permissions can be checked on the model.


   .. py:attribute:: owner


   .. py:attribute:: roles


   .. py:attribute:: access_requests


   .. py:attribute:: enrollment_methods


   .. py:attribute:: role_assignments


   .. py:attribute:: public_permissions


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: content_type_is_scope(content_type)
      :staticmethod:


      Check whether the given content type implements `ScopedRolesMixin` and therefor acts as
      a permission scope for user roles.



   .. py:method:: get_scope_model_content_types()
      :classmethod:


      Get a filtered list of content types (models) that implement the scoped roles mixin and
      therefor act as a permission scope for user roles. Since this is a somewhat expensive
      operation, the result will be cached using the Django cache mechanism.



   .. py:method:: get_scope_model_content_type_ids()
      :classmethod:


      Get content type ids of models that are permission scopes for user roles.



   .. py:method:: save(*args, **kwargs)

      Automatically populate the `owner` field.
      Care must be taken to call `super().save(*args, **kwargs)` when this method is overridden.



.. py:class:: ScopeMixin(*args, **kwargs)

   Bases: :py:obj:`RoleBasedObjectPermissionsMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.mixins.scope.ScopeMixin
      :parts: 1


   Abstract mixin for models that are linked to a scope via a generic relation. The scope will be
   used for role assignments to assign scoped roles to users. This is used internally to add a
   generic relation for the scope to models like `AccessRequest` or `EnrollmentMethod`.


   .. py:attribute:: scope_type


   .. py:attribute:: scope_uuid


   .. py:attribute:: scope_object


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: from_obj(other_obj, **kwargs)
      :classmethod:


      Create a new instance from another scope-related model instance, copying over the
      scope reference and optionally the role.



   .. py:method:: clean()

      Validate that role and this object refer to the same scope (if `role` field exists).



   .. py:method:: get_scope()

      Access management requires appropriate permissions in the referenced scope.



   .. py:method:: has_obj_perm(user_obj, perm)

      Object-level permission for all models with a scope reference. If this is a role,
      its priority must be of lower or equal priority than any of the user's roles.
      Otherwise the priority of the referenced role must be of lower or equal priority
      than any of the user's roles.



