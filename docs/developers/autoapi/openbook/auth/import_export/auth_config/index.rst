openbook.auth.import_export.auth_config
=======================================

.. py:module:: openbook.auth.import_export.auth_config


Classes
-------

.. autoapisummary::

   openbook.auth.import_export.auth_config.AuthConfigForeignKeyWidget


Module Contents
---------------

.. py:class:: AuthConfigForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.auth_config.AuthConfigForeignKeyWidget
      :parts: 1


   Widget for a ``ForeignKey`` field which looks up a related model using
   either the PK or a user specified field that uniquely identifies the
   instance in both export and import.

   The lookup field defaults to using the primary key (``pk``) as lookup
   criterion but can be customized to use any field on the related model.

   Unlike specifying a related field in your resource like so…

   ::

       class Meta:
           fields = ('author__name',)

   …using a :class:`~import_export.widgets.ForeignKeyWidget` has the
   advantage that it can not only be used for exporting, but also importing
   data with foreign key relationships.

   Here's an example on how to use
   :class:`~import_export.widgets.ForeignKeyWidget` to lookup related objects
   using ``Author.name`` instead of ``Author.pk``::

       from import_export import fields, resources
       from import_export.widgets import ForeignKeyWidget

       class BookResource(resources.ModelResource):
           author = fields.Field(
               column_name='author',
               attribute='author',
               widget=ForeignKeyWidget(Author, 'name'))

           class Meta:
               fields = ('author',)

   :param model: The Model the ForeignKey refers to (required).
   :param field: A field on the related model used for looking up a particular
       object.
   :param use_natural_foreign_keys: Use natural key functions to identify
       related object, default to False


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



