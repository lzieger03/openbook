openbook.core.models.utils.json
===============================

.. py:module:: openbook.core.models.utils.json


Classes
-------

.. autoapisummary::

   openbook.core.models.utils.json.PrettyPrintJSONEncoder


Module Contents
---------------

.. py:class:: PrettyPrintJSONEncoder(*args, indent, sort_keys, **kwargs)

   Bases: :py:obj:`json.JSONEncoder`

   .. autoapi-inheritance-diagram:: openbook.core.models.utils.json.PrettyPrintJSONEncoder
      :parts: 1


   JSON encoder with pretty printing to make sure that saved values are indented
   for easier editing in the Django admin. See: https://unfoldadmin.com/docs/fields/json/


