openbook.auth.admin.role
========================

.. py:module:: openbook.auth.admin.role


Classes
-------

.. autoapisummary::

   openbook.auth.admin.role.RoleResource
   openbook.auth.admin.role.RoleForm
   openbook.auth.admin.role.RoleInline
   openbook.auth.admin.role.RoleAdmin


Module Contents
---------------

.. py:class:: RoleResource

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeResourceMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role.RoleResource
      :parts: 1


   .. py:attribute:: is_active


   .. py:attribute:: permissions


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: RoleForm

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeFormMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role.RoleForm
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: '__all__'




   .. py:class:: Media

      .. py:attribute:: css


      .. py:attribute:: js



   .. py:method:: clean()

      Check that only allowed permissions are assigned.



.. py:class:: RoleInline(parent_model, admin_site)

   Bases: :py:obj:`django.contrib.contenttypes.admin.GenericTabularInline`, :py:obj:`unfold.admin.TabularInline`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role.RoleInline
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
      :value: ['priority', 'name', 'slug', 'is_active']



   .. py:attribute:: ordering
      :value: ['priority', 'name']



   .. py:attribute:: readonly_fields
      :value: []



   .. py:attribute:: prepopulated_fields


   .. py:attribute:: extra
      :value: 0



   .. py:attribute:: show_change_link
      :value: True



   .. py:attribute:: tab
      :value: True



.. py:class:: RoleAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.role.RoleAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display


   .. py:attribute:: list_display_links
      :value: ['scope_type', 'scope_object', 'priority', 'name', 'slug']



   .. py:attribute:: list_filter


   .. py:attribute:: list_sections


   .. py:attribute:: list_select_related


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'priority', 'name']



   .. py:attribute:: search_fields
      :value: ['name', 'slug', 'description']



   .. py:attribute:: readonly_fields


   .. py:attribute:: prepopulated_fields


   .. py:attribute:: filter_horizontal
      :value: ['permissions']



   .. py:attribute:: inlines


   .. py:method:: get_queryset(request)

      Prefetch relations to optimize database performance for the changelist sections.



   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


