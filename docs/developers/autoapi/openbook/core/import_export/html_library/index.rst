openbook.core.import_export.html_library
========================================

.. py:module:: openbook.core.import_export.html_library


Classes
-------

.. autoapisummary::

   openbook.core.import_export.html_library.HTMLLibraryForeignKeyWidget
   openbook.core.import_export.html_library.HTMLLibraryVersionForeignKeyWidget


Module Contents
---------------

.. py:class:: HTMLLibraryForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.core.import_export.html_library.HTMLLibraryForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports HTML libraries as
   npm-style strings: `@organization/library`-


   .. py:method:: render(value, row=None, **kwargs)

      :return: A string representation of the related value.
        If ``use_natural_foreign_keys``, the value's natural key is returned.
        ``coerce_to_string`` has no effect on the return value.



   .. py:method:: clean(value, obj=None, **kwargs)

      :return: a single Foreign Key instance derived from the args.
        ``None`` can be returned if the value passed is a null value.

      :param value: The field's value in the dataset.
      :param row: The dataset's current row.
      :param \**kwargs:
          Optional kwargs.
      :raises: ``ObjectDoesNotExist`` if no valid instance can be found.



.. py:class:: HTMLLibraryVersionForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.core.import_export.html_library.HTMLLibraryVersionForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports HTML library versions as
   npm-style strings: `@organization/library 1.0.0`-


   .. py:method:: render(value, row=None, **kwargs)

      :return: A string representation of the related value.
        If ``use_natural_foreign_keys``, the value's natural key is returned.
        ``coerce_to_string`` has no effect on the return value.



   .. py:method:: clean(value, obj=None, **kwargs)

      :return: a single Foreign Key instance derived from the args.
        ``None`` can be returned if the value passed is a null value.

      :param value: The field's value in the dataset.
      :param row: The dataset's current row.
      :param \**kwargs:
          Optional kwargs.
      :raises: ``ObjectDoesNotExist`` if no valid instance can be found.



