openbook.core.admin.utils.model
===============================

.. py:module:: openbook.core.admin.utils.model


Classes
-------

.. autoapisummary::

   openbook.core.admin.utils.model.ModelAdmin


Module Contents
---------------

.. py:class:: ModelAdmin(model, admin_site)

   Bases: :py:obj:`unfold.admin.ModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.core.admin.utils.model.ModelAdmin
      :parts: 1


   Improved version of the stock `ModelAdmin` that checks object-permissions instead of
   the regular model-permissions. The only difference is, that `obj` will be set to the
   object to be viewed/changed/deleted, when the permission is checked.

   This relies on our custom authentication backend to fallback to regular permissions
   checks when the object doesn't support object-permissions or the object-based permission
   check fails.


   .. py:method:: save_form(request, form, change)

      The parent class calls `has_add_permission()` in `_changeform_view()` just before the form
      data is validated and saved, but doesn't have the new object, yet. Therefor `has_add_permission()`
      lacks the `obj` parameter. This method is called after the validation to actually save the object.
      As a hacky workaround we catch up on the permission check here.



   .. py:method:: has_view_permission(request, obj = None)

      The base class also checks "change" permission, when "view" fails. This logic was moved
      to our custom authentication backend.



   .. py:method:: has_change_permission(request, obj = None)

      Return True if the given request has permission to change the given
      Django model instance, the default implementation doesn't examine the
      `obj` parameter.

      Can be overridden by the user in subclasses. In such case it should
      return True if the given request has permission to change the `obj`
      model instance. If `obj` is None, this should return True if the given
      request has permission to change *any* object of the given type.



   .. py:method:: has_delete_permission(request, obj = None)

      Return True if the given request has permission to delete the given
      Django model instance, the default implementation doesn't examine the
      `obj` parameter.

      Can be overridden by the user in subclasses. In such case it should
      return True if the given request has permission to delete the `obj`
      model instance. If `obj` is None, this should return True if the given
      request has permission to delete *any* object of the given type.



