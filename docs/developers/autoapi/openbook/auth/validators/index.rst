openbook.auth.validators
========================

.. py:module:: openbook.auth.validators


Functions
---------

.. autoapisummary::

   openbook.auth.validators.validate_scope_type
   openbook.auth.validators.validate_permissions


Module Contents
---------------

.. py:function:: validate_scope_type(scope_type)

   Check that only valid scope types are assigned where the model class implements
   the `ScopedRolesMixin`.


.. py:function:: validate_permissions(scope_type, permissions)

   Check that only allowed permissions are assigned. Does nothing if either value
   is missing or only allowed permissions are used. Otherwise a `ValidationError`
   is raised.


