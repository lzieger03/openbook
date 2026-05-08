openbook.auth.backends
======================

.. py:module:: openbook.auth.backends


Classes
-------

.. autoapisummary::

   openbook.auth.backends.RoleBasedObjectPermissionsBackend


Module Contents
---------------

.. py:class:: RoleBasedObjectPermissionsBackend

   Bases: :py:obj:`django.contrib.auth.backends.ModelBackend`

   .. autoapi-inheritance-diagram:: openbook.auth.backends.RoleBasedObjectPermissionsBackend
      :parts: 1


   Customized version of the stock model authentication backend. For normal permission checks
   without an object it behaves exactly the same. Object permissions are checked in the following
   order, stopping at the first match:

   1. The user is a superuser
   2. The user and the object are the same
   3. The user is the object's `owner` (optional).
   4. The object's `has_obj_perm()` method (optional).
   5. Regular non-object permissions

   Superusers can do anything. Users can change their own data. The owner is always authorized.
   Otherwise role-based permissions are checked. If this is not supported by the object or fails,
   we fall back to regular user permissions. Thus, the `ModelBackend` doesn't need to be included
   in the Django settings, as its function is already covered here.


   .. py:method:: has_perm(user_obj, perm, obj=None)


