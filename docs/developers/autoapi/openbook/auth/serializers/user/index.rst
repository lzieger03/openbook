openbook.auth.serializers.user
==============================

.. py:module:: openbook.auth.serializers.user


Classes
-------

.. autoapisummary::

   openbook.auth.serializers.user.UserField


Module Contents
---------------

.. py:class:: UserField(**kwargs)

   Bases: :py:obj:`rest_framework.serializers.SlugRelatedField`

   .. autoapi-inheritance-diagram:: openbook.auth.serializers.user.UserField
      :parts: 1


   Serializer field to use the username for input and output instead of a user's raw PK.


   .. py:method:: get_queryset()


