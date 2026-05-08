openbook.core.utils.content_type
================================

.. py:module:: openbook.core.utils.content_type


Functions
---------

.. autoapisummary::

   openbook.core.utils.content_type.model_string_for_content_type
   openbook.core.utils.content_type.content_type_for_model_string


Module Contents
---------------

.. py:function:: model_string_for_content_type(content_type)

   Serialize content type objet into model string as used by Django: `{app_label}.{model}`


.. py:function:: content_type_for_model_string(model_string)

   Get content type object for a given model string or raise `ContentType.DoesNotExist`,
   when the content type cannot be found.


