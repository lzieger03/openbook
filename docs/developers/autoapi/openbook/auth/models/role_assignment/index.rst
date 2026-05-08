openbook.auth.models.role_assignment
====================================

.. py:module:: openbook.auth.models.role_assignment


Classes
-------

.. autoapisummary::

   openbook.auth.models.role_assignment.RoleAssignment


Module Contents
---------------

.. py:class:: RoleAssignment

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.auth.models.mixins.scope.ScopeMixin`, :py:obj:`openbook.core.models.mixins.active.ActiveInactiveMixin`, :py:obj:`openbook.core.models.mixins.datetime.ValidityTimeSpanMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.role_assignment.RoleAssignment
      :parts: 1


   A role assignment assigns a given role (defined in a given scope) to a user, effectively
   granting the object-level permissions associated with them.


   .. py:class:: AssignmentMethod

      Bases: :py:obj:`django.db.models.TextChoices`

      .. autoapi-inheritance-diagram:: openbook.auth.models.role_assignment.RoleAssignment.AssignmentMethod
         :parts: 1


      Class for creating enumerated string choices.


      .. py:attribute:: MANUAL


      .. py:attribute:: SELF_ENROLLMENT


      .. py:attribute:: ACCESS_REQUEST



   .. py:attribute:: role


   .. py:attribute:: user


   .. py:attribute:: assignment_method


   .. py:attribute:: enrollment_method


   .. py:attribute:: access_request


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints


      .. py:attribute:: indexes



   .. py:method:: clean()

      Set assignment method to manual, when it is empty. Needed for the Django Admin, because
      this field cannot be set manually.



   .. py:method:: enroll(enrollment, user = None, passphrase = None, check_passphrase = True, permission_user = None, check_permission = True)
      :classmethod:


      Apply the given enrollment method or access request to a user, effectively adding the role
      assignment. For access requests the user should not be given, as it is already contained
      in the access request object. For enrollment methods it must be given, however.

      Raises `PermissionDenied` when the `permission_user` or the current request users lacks
      the `openbook_auth.add_roleassignment` permission.

      Also raises a `PermissionDenied` when the passphrase doesn't match or the user is missing.



   .. py:method:: withdraw(enrollment, user = None, permission_user = None, check_permission = True)
      :classmethod:


      Withdraw role assignment for a given enrollment method or access request. For access requests the
      user should not be given, as it is already contained in the access request object. For enrollment
      methods it must be given, however.

      Raises a `ValueError` when the user is missing.

      Raises `PermissionDenied` when the `permission_user` or the current request users lacks
      the `openbook_auth.delete_roleassignment` permission.



