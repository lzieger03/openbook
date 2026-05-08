openbook.core.models.mixins.text
================================

.. py:module:: openbook.core.models.mixins.text


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.text.NameDescriptionMixin


Module Contents
---------------

.. py:class:: NameDescriptionMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.text.NameDescriptionMixin
      :parts: 1


   Mixin for models with a clear-text short name and long description in either plain text,
   HTML or Markdown format.


   .. py:class:: TextFormatChoices

      Bases: :py:obj:`django.db.models.TextChoices`

      .. autoapi-inheritance-diagram:: openbook.core.models.mixins.text.NameDescriptionMixin.TextFormatChoices
         :parts: 1


      Formatted text content can either be in plain text, HTML or Markdown format.


      .. py:attribute:: PLAIN_TEXT


      .. py:attribute:: HTML


      .. py:attribute:: MARKDOWN



   .. py:attribute:: name


   .. py:attribute:: description


   .. py:attribute:: text_format


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: get_formatted_description()

      Return the description in a format that can be directly embedded into HTML.

      If the description is in HTML format, it will be returned as is. If it is in Markdown format,
      it will be converted to HTML first. If it is in plain text format, it will be wrapped in a
      `<pre>` tag.



