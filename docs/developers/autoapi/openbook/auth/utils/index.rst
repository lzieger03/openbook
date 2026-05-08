openbook.auth.utils
===================

.. py:module:: openbook.auth.utils


Functions
---------

.. autoapisummary::

   openbook.auth.utils.perm_name_for_permission
   openbook.auth.utils.perm_string_for_permission
   openbook.auth.utils.app_label_for_permission
   openbook.auth.utils.app_name_for_permission
   openbook.auth.utils.model_for_permission
   openbook.auth.utils.model_name_for_permission
   openbook.auth.utils.permission_for_perm_string


Module Contents
---------------

.. py:function:: perm_name_for_permission(permission)

   Get clear-text, translated permission name from permission object.


.. py:function:: perm_string_for_permission(permission)

   Serialize permission object into permission string as used by Django:
   `{app_label}.{codename}`


.. py:function:: app_label_for_permission(permission)

   Get app label from permission object.


.. py:function:: app_name_for_permission(permission)

   Get translated app name from permission object


.. py:function:: model_for_permission(permission)

   Get model label from permission object.


.. py:function:: model_name_for_permission(permission)

   Get translated modal name from permission object.


.. py:function:: permission_for_perm_string(perm)

   Get permission object for a given permission string or raise `Permission.DoesNotExist`,
   when the permission cannot be found.


