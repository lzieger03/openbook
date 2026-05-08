openbook.auth.import_export.user
================================

.. py:module:: openbook.auth.import_export.user


Classes
-------

.. autoapisummary::

   openbook.auth.import_export.user.UserForeignKeyWidget
   openbook.auth.import_export.user.UserManyToManyWidget


Module Contents
---------------

.. py:class:: UserForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.user.UserForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports users with their username.


.. py:class:: UserManyToManyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ManyToManyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.user.UserManyToManyWidget
      :parts: 1


   A customized many-to-many widget that exports and imports users with their username.


