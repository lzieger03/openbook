openbook.auth.serializers.permission
====================================

.. py:module:: openbook.auth.serializers.permission


Classes
-------

.. autoapisummary::

   openbook.auth.serializers.permission.PermissionField


Module Contents
---------------

.. py:class:: PermissionField(**kwargs)

   Bases: :py:obj:`rest_framework.serializers.RelatedField`

   .. autoapi-inheritance-diagram:: openbook.auth.serializers.permission.PermissionField
      :parts: 1


   Serializer field to use permission string as input and output instead of a
   permission's raw PK.


   .. py:attribute:: default_error_messages


   .. py:method:: get_queryset()


   .. py:method:: to_internal_value(data)

      Transform the *incoming* primitive data into a native value.



   .. py:method:: to_representation(obj)

      Transform the *outgoing* native value into primitive data.



