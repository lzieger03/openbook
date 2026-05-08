openbook.core.models.language
=============================

.. py:module:: openbook.core.models.language


Classes
-------

.. autoapisummary::

   openbook.core.models.language.Language


Module Contents
---------------

.. py:class:: Language(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.language.Language
      :parts: 1


   Simple data model for available languages. Administrators need to customize a list of
   languages that should be supported by the installation. This allows to maintain translations
   of these langauges for all translatable database models.

   NOTE: Some translated texts come from the application itself. They need to be translated
   with the Django `manage.py` command and gettext.


   .. py:attribute:: language


   .. py:attribute:: name


