openbook.core.models.mixins.file
================================

.. py:module:: openbook.core.models.mixins.file


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.file.FileUploadMixin


Module Contents
---------------

.. py:class:: FileUploadMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.file.FileUploadMixin
      :parts: 1


   Abstract base class for the generic file upload models below. Contains the common
   fields for the file data and meta data, which are populated when the model is saved.


   .. py:method:: calc_file_path_hook(filename)

      To be overridden by implementing class.



   .. py:attribute:: file_data


   .. py:attribute:: file_name


   .. py:attribute:: file_size


   .. py:attribute:: mime_type


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: save(*args, **kwargs)

      Populate meta-data fields when file is saved.



