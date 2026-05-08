openbook.core.import_export.site
================================

.. py:module:: openbook.core.import_export.site


Classes
-------

.. autoapisummary::

   openbook.core.import_export.site.SiteForeignKeyWidget


Module Contents
---------------

.. py:class:: SiteForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.core.import_export.site.SiteForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports sites as domain strings.


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



