openbook.drf.flex_serializers
=============================

.. py:module:: openbook.drf.flex_serializers


Classes
-------

.. autoapisummary::

   openbook.drf.flex_serializers.FlexFieldsModelSerializer


Module Contents
---------------

.. py:class:: FlexFieldsModelSerializer(*args, **kwargs)

   Bases: :py:obj:`rest_flex_fields2.serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.drf.flex_serializers.FlexFieldsModelSerializer
      :parts: 1


   Reuse full cleaning and validation logic of the models in the REST API, including
   `full_clean()`, `clean()`, field validation and uniqueness checks. Also make sure,
   that the pre-filled model instance can be accessed in the DRF view.
   ```


   .. py:method:: validate(attrs)


   .. py:method:: get_prefilled_instance()

      Method to access the pre-filled model instance in `ModelViewSetMixin`.



