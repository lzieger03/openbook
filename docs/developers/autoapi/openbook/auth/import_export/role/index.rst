openbook.auth.import_export.role
================================

.. py:module:: openbook.auth.import_export.role


Classes
-------

.. autoapisummary::

   openbook.auth.import_export.role.RoleForeignKeyWidget
   openbook.auth.import_export.role.RoleManyToManyWidget


Module Contents
---------------

.. py:class:: RoleForeignKeyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ForeignKeyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.role.RoleForeignKeyWidget
      :parts: 1


   A customized foreign-key widget that exports and imports roles with their slug.


.. py:class:: RoleManyToManyWidget(*args, **kwargs)

   Bases: :py:obj:`import_export.widgets.ManyToManyWidget`

   .. autoapi-inheritance-diagram:: openbook.auth.import_export.role.RoleManyToManyWidget
      :parts: 1


   A customized many-to-many widget that exports and imports roles with their slug.


