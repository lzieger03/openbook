openbook.auth.import_export.group
=================================

.. py:module:: openbook.auth.import_export.group


Classes
-------

.. autoapisummary::

   openbook.auth.import_export.group.GroupForeignKeyWidget
   openbook.auth.import_export.group.GroupManyToManyWidget


Module Contents
---------------

.. py:class:: GroupForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.group.GroupForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports groups with their slug.


.. py:class:: GroupManyToManyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ManyToManyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.group.GroupManyToManyWidget
      :parts: 1


   A customized many-to-many widget that exports and imports groups with their slug.


