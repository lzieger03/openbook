openbook.core.models.utils.file
===============================

.. py:module:: openbook.core.models.utils.file


Functions
---------

.. autoapisummary::

   openbook.core.models.utils.file.calc_file_path


Module Contents
---------------

.. py:function:: calc_file_path(object, pk, filename)

   Callable for the `upload_to` property of `model.FileField`. Determines the upload path
   by joining the app label and model name.

   The first parameter normally is the model's `_meta` attribute. But `self.content_type`,
   if it is a `models.ForeignKey` from a generic relation, can make sense to use the app
   name and label of the foreign model, instead.


