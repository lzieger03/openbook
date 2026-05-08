openbook.drf.permissions
========================

.. py:module:: openbook.drf.permissions


Classes
-------

.. autoapisummary::

   openbook.drf.permissions.DjangoObjectPermissionsOnly


Module Contents
---------------

.. py:class:: DjangoObjectPermissionsOnly

   Bases: :py:obj:`rest_framework.permissions.DjangoObjectPermissions`

   .. autoapi-inheritance-diagram:: openbook.drf.permissions.DjangoObjectPermissionsOnly
      :parts: 1


   Class `APIView`, which is a parent for `ModelViewSet` in Django REST Framework the method
   `check_permissions()` is called very early and later `check_object_permissions()`, too.
   Since `DjangoObjectPermissions` is a `DjangoModelPermissions` it implements both checks.
   But DRF raises an exception when either method returns `False`, thus inverting the logic
   in our own authentication backend. Also both classes don't check "view" permissions by default.

   This class replaces `DjangoObjectPermissions` with a version more in line with our own backend.


   .. py:attribute:: perms_map


   .. py:method:: has_permission(request, view)

      Return `True` if permission is granted, `False` otherwise.



