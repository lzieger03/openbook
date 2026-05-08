openbook.auth.serializers.mixins.scope
======================================

.. py:module:: openbook.auth.serializers.mixins.scope


Classes
-------

.. autoapisummary::

   openbook.auth.serializers.mixins.scope.ScopedRolesSerializerMixin
   openbook.auth.serializers.mixins.scope.ScopeTypeField


Module Contents
---------------

.. py:class:: ScopedRolesSerializerMixin(*args, **kwargs)

   Bases: :py:obj:`rest_flex_fields2.serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.serializers.mixins.scope.ScopedRolesSerializerMixin
      :parts: 1


   Mixin class for model serializers whose models implement the `ScopedRolesMixin` and as such
   act as permission scope for user roles. Default serializer, that adds all scope fields.


   .. py:attribute:: owner


   .. py:attribute:: public_permissions


   .. py:attribute:: role_assignments


   .. py:attribute:: enrollment_methods


   .. py:attribute:: access_requests


   .. py:class:: Meta

      .. py:attribute:: fields
         :value: ('owner', 'public_permissions', 'role_assignments', 'enrollment_methods', 'access_requests')



      .. py:attribute:: read_only_fields
         :value: ('role_assignments', 'enrollment_methods', 'access_requests')



      .. py:attribute:: expandable_fields



   .. py:method:: validate(attributes)

      Check that only allowed permissions are assigned.



.. py:class:: ScopeTypeField(**kwargs)

   Bases: :py:obj:`rest_framework.serializers.RelatedField`

   .. autoapi-inheritance-diagram:: openbook.auth.serializers.mixins.scope.ScopeTypeField
      :parts: 1


   Serializer field for the `scope_type` to use the fully-qualified model name instead
   of the PK for input and output.


   .. py:attribute:: default_error_messages


   .. py:method:: get_queryset()


   .. py:method:: to_internal_value(data)

      Transform the *incoming* primitive data into a native value.



   .. py:method:: to_representation(obj)

      Transform the *outgoing* native value into primitive data.



