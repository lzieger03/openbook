openbook.core.import_export.boolean
===================================

.. py:module:: openbook.core.import_export.boolean


Classes
-------

.. autoapisummary::

   openbook.core.import_export.boolean.BooleanWidget


Module Contents
---------------

.. py:class:: BooleanWidget(coerce_to_string=True)

   Bases: :py:obj:`import_export.widgets.BooleanWidget`

   .. autoapi-inheritance-diagram:: openbook.core.import_export.boolean.BooleanWidget
      :parts: 1


   A customized boolean widget that renders its value as "true" and "false"
   instead of zero and one.


   .. py:method:: render(value, row=None, **kwargs)

      :return: ``True`` is represented as ``1``, ``False`` as ``0``, and
        ``None``/NULL as an empty string.

        If ``coerce_to_string`` is ``False``, the python Boolean type is
        returned (may be ``None``).



   .. py:method:: clean(value, obj=None, **kwargs)

      Converts the input value to a Python boolean or None.

      Recognizes common string representations of boolean values:
      - True values: '1', 1, True, 'true', 'TRUE', 'True'
      - False values: '0', 0, False, 'false', 'FALSE', 'False'
      - Null values: '', None, 'null', 'NULL', 'none', 'NONE', 'None'

      :param value: The value to be converted to boolean.
      :param row: The current row being processed.
      :param **kwargs: Optional keyword arguments.
      :returns: True, False, or None depending on the input value.



