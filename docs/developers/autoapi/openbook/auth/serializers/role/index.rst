openbook.auth.serializers.role
==============================

.. py:module:: openbook.auth.serializers.role


Classes
-------

.. autoapisummary::

   openbook.auth.serializers.role.RoleField


Module Contents
---------------

.. py:class:: RoleField(**kwargs)

   Bases: :py:obj:`rest_framework.serializers.RelatedField`

   .. autoapi-inheritance-diagram:: openbook.auth.serializers.role.RoleField
      :parts: 1


   Serializer field to use slug as input and output instead of a role's raw PK.


   .. py:attribute:: default_error_messages


   .. py:method:: get_queryset()


   .. py:method:: to_internal_value(data)

      Transform the *incoming* primitive data into a native value.



   .. py:method:: to_representation(obj)

      Transform the *outgoing* native value into primitive data.



