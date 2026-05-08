openbook.auth.admin.access_request
==================================

.. py:module:: openbook.auth.admin.access_request


Classes
-------

.. autoapisummary::

   openbook.auth.admin.access_request.AccessRequestResource
   openbook.auth.admin.access_request.AccessRequestForm
   openbook.auth.admin.access_request.AccessRequestInline
   openbook.auth.admin.access_request.AccessRequestAdmin


Module Contents
---------------

.. py:class:: AccessRequestResource

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeResourceMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.access_request.AccessRequestResource
      :parts: 1


   .. py:attribute:: user


   .. py:attribute:: role


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: AccessRequestForm

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeFormMixin`, :py:obj:`openbook.auth.admin.mixins.scope.ScopeRoleFieldFormMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.access_request.AccessRequestForm
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: '__all__'




   .. py:class:: Media

      .. py:attribute:: css


      .. py:attribute:: js



.. py:class:: AccessRequestInline(parent_model, admin_site)

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeRoleFieldInlineMixin`, :py:obj:`django.contrib.contenttypes.admin.GenericTabularInline`, :py:obj:`unfold.admin.TabularInline`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.access_request.AccessRequestInline
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
      :value: ['user', 'role', 'decision', 'decision_date']



   .. py:attribute:: ordering
      :value: ['user', 'role']



   .. py:attribute:: readonly_fields
      :value: ['user', 'role', 'decision_date']



   .. py:attribute:: extra
      :value: 0



   .. py:attribute:: show_change_link
      :value: True



   .. py:attribute:: tab
      :value: True



   .. py:method:: has_add_permission(*args, **kwargs)

      Return True if the given request has permission to add an object.
      Can be overridden by the user in subclasses.



.. py:class:: AccessRequestAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.access_request.AccessRequestAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display


   .. py:attribute:: list_display_links
      :value: ['scope_type', 'scope_object', 'role', 'user']



   .. py:attribute:: list_select_related


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'role', 'user']



   .. py:attribute:: search_fields
      :value: ['role__name', 'user__username', 'user__first_name', 'user__last_name']



   .. py:attribute:: readonly_fields


   .. py:attribute:: list_filter


   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


