openbook.auth.admin.enrollment_method
=====================================

.. py:module:: openbook.auth.admin.enrollment_method


Classes
-------

.. autoapisummary::

   openbook.auth.admin.enrollment_method.EnrollmentMethodResource
   openbook.auth.admin.enrollment_method.EnrollmentMethodForm
   openbook.auth.admin.enrollment_method.EnrollmentMethodInline
   openbook.auth.admin.enrollment_method.EnrollmentMethodAdmin


Module Contents
---------------

.. py:class:: EnrollmentMethodResource

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeResourceMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.enrollment_method.EnrollmentMethodResource
      :parts: 1


   .. py:attribute:: role


   .. py:attribute:: is_active


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: EnrollmentMethodForm

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeFormMixin`, :py:obj:`openbook.auth.admin.mixins.scope.ScopeRoleFieldFormMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.enrollment_method.EnrollmentMethodForm
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: '__all__'




   .. py:class:: Media

      .. py:attribute:: css


      .. py:attribute:: js



.. py:class:: EnrollmentMethodInline(parent_model, admin_site)

   Bases: :py:obj:`openbook.auth.admin.mixins.scope.ScopeRoleFieldInlineMixin`, :py:obj:`django.contrib.contenttypes.admin.GenericTabularInline`, :py:obj:`unfold.admin.TabularInline`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.enrollment_method.EnrollmentMethodInline
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
      :value: ['name', 'role', 'is_active', 'passphrase']



   .. py:attribute:: ordering
      :value: ['name', 'role']



   .. py:attribute:: extra
      :value: 0



   .. py:attribute:: show_change_link
      :value: True



   .. py:attribute:: tab
      :value: True



.. py:class:: EnrollmentMethodAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.admin.enrollment_method.EnrollmentMethodAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: form


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display


   .. py:attribute:: list_display_links
      :value: ['scope_type', 'scope_object', 'name', 'role']



   .. py:attribute:: list_select_related


   .. py:attribute:: ordering
      :value: ['scope_type', 'scope_uuid', 'name', 'role']



   .. py:attribute:: search_fields
      :value: ['name', 'role__name', 'user__username']



   .. py:attribute:: readonly_fields


   .. py:attribute:: list_filter


   .. py:attribute:: fieldsets


   .. py:attribute:: add_fieldsets


