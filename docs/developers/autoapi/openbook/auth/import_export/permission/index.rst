openbook.auth.import_export.permission
======================================

.. py:module:: openbook.auth.import_export.permission


Classes
-------

.. autoapisummary::

   openbook.auth.import_export.permission.PermissionForeignKeyWidget
   openbook.auth.import_export.permission.PermissionManyToManyWidget


Module Contents
---------------

.. py:class:: PermissionForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.permission.PermissionForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports permissions as
   Django-style permission strings.


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



.. py:class:: PermissionManyToManyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ManyToManyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.permission.PermissionManyToManyWidget
      :parts: 1


   A customized many-to-many widget that exports and imports permissions as
   Django-style permission strings.


   .. py:method:: render(value, row=None, **kwargs)

      :return: A string with values separated by ``separator``.
        ``None`` values are returned as empty strings.
        ``coerce_to_string`` has no effect on the return value.



   .. py:method:: clean(value, obj=None, **kwargs)

      Converts a separated string of values into a QuerySet for ManyToMany
      relationships.

      Splits the input by the configured separator and looks up model instances
      using the specified field. Filters out empty values after splitting.

      :param value: String of separated values, or a single numeric value.
      :param row: The current row being processed.
      :param **kwargs: Optional keyword arguments.
      :returns: A QuerySet containing the related model instances, or an empty
          QuerySet
          if no value provided.



