openbook.auth.viewsets.scope
============================

.. py:module:: openbook.auth.viewsets.scope


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.scope.AllowedPermissionSerializer
   openbook.auth.viewsets.scope.ScopeObjectSerializer
   openbook.auth.viewsets.scope.ScopeTypeRetrieveSerializer
   openbook.auth.viewsets.scope.ScopeTypeListSerializer
   openbook.auth.viewsets.scope.ScopeTypeViewSet


Module Contents
---------------

.. py:class:: AllowedPermissionSerializer(instance=None, data=empty, **kwargs)

   Bases: :py:obj:`rest_framework.serializers.Serializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.scope.AllowedPermissionSerializer
      :parts: 1


   The BaseSerializer class provides a minimal class which may be used
   for writing custom serializer implementations.

   Note that we strongly restrict the ordering of operations/properties
   that may be used on the serializer in order to enforce correct usage.

   In particular, if a `data=` argument is passed then:

   .is_valid() - Available.
   .initial_data - Available.
   .validated_data - Only available after calling `is_valid()`
   .errors - Only available after calling `is_valid()`
   .data - Only available after calling `is_valid()`

   If a `data=` argument is not passed then:

   .is_valid() - Not available.
   .initial_data - Not available.
   .validated_data - Not available.
   .errors - Not available.
   .data - Available.


   .. py:attribute:: id


   .. py:attribute:: perm


   .. py:attribute:: app


   .. py:attribute:: model


   .. py:attribute:: name


.. py:class:: ScopeObjectSerializer(instance=None, data=empty, **kwargs)

   Bases: :py:obj:`rest_framework.serializers.Serializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.scope.ScopeObjectSerializer
      :parts: 1


   The BaseSerializer class provides a minimal class which may be used
   for writing custom serializer implementations.

   Note that we strongly restrict the ordering of operations/properties
   that may be used on the serializer in order to enforce correct usage.

   In particular, if a `data=` argument is passed then:

   .is_valid() - Available.
   .initial_data - Available.
   .validated_data - Only available after calling `is_valid()`
   .errors - Only available after calling `is_valid()`
   .data - Only available after calling `is_valid()`

   If a `data=` argument is not passed then:

   .is_valid() - Not available.
   .initial_data - Not available.
   .validated_data - Not available.
   .errors - Not available.
   .data - Available.


   .. py:attribute:: uuid


   .. py:attribute:: name


.. py:class:: ScopeTypeRetrieveSerializer(instance=None, data=empty, **kwargs)

   Bases: :py:obj:`rest_framework.serializers.Serializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.scope.ScopeTypeRetrieveSerializer
      :parts: 1


   The BaseSerializer class provides a minimal class which may be used
   for writing custom serializer implementations.

   Note that we strongly restrict the ordering of operations/properties
   that may be used on the serializer in order to enforce correct usage.

   In particular, if a `data=` argument is passed then:

   .is_valid() - Available.
   .initial_data - Available.
   .validated_data - Only available after calling `is_valid()`
   .errors - Only available after calling `is_valid()`
   .data - Only available after calling `is_valid()`

   If a `data=` argument is not passed then:

   .is_valid() - Not available.
   .initial_data - Not available.
   .validated_data - Not available.
   .errors - Not available.
   .data - Available.


   .. py:attribute:: pk


   .. py:attribute:: id


   .. py:attribute:: label


   .. py:attribute:: objects


   .. py:attribute:: allowed_permissions


.. py:class:: ScopeTypeListSerializer(instance=None, data=empty, **kwargs)

   Bases: :py:obj:`rest_framework.serializers.Serializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.scope.ScopeTypeListSerializer
      :parts: 1


   The BaseSerializer class provides a minimal class which may be used
   for writing custom serializer implementations.

   Note that we strongly restrict the ordering of operations/properties
   that may be used on the serializer in order to enforce correct usage.

   In particular, if a `data=` argument is passed then:

   .is_valid() - Available.
   .initial_data - Available.
   .validated_data - Only available after calling `is_valid()`
   .errors - Only available after calling `is_valid()`
   .data - Only available after calling `is_valid()`

   If a `data=` argument is not passed then:

   .is_valid() - Not available.
   .initial_data - Not available.
   .validated_data - Not available.
   .errors - Not available.
   .data - Available.


   .. py:attribute:: pk


   .. py:attribute:: id


   .. py:attribute:: label


.. py:class:: ScopeTypeViewSet(**kwargs)

   Bases: :py:obj:`rest_framework.viewsets.ViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.scope.ScopeTypeViewSet
      :parts: 1


   Permission scopes. When a list is requested, a flat list of scope types will be returned.
   If a single object is requested, full details including all scopes and allowed permissions
   will be returned.


   .. py:attribute:: permission_classes


   .. py:attribute:: pagination_class
      :value: None



   .. py:attribute:: filter_backends
      :value: []



   .. py:attribute:: queryset


   .. py:attribute:: lookup_field
      :value: 'id'



   .. py:attribute:: lookup_value_regex
      :value: '[^/]+'



   .. py:attribute:: ordering
      :value: ['id']



   .. py:method:: list(request, *args, **kwargs)

      GET List: Return a flat list of scope types.



   .. py:method:: retrieve(request, *args, **kwargs)

      GET Scope Type: Return an object with all scopes and allowed permissions.



