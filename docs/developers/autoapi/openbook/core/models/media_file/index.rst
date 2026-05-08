openbook.core.models.media_file
===============================

.. py:module:: openbook.core.models.media_file


Classes
-------

.. autoapisummary::

   openbook.core.models.media_file.MediaFile


Module Contents
---------------

.. py:class:: MediaFile(*args, **kwargs)

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.file.FileUploadMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.core.models.media_file.MediaFile
      :parts: 1


   Generic model for media files, when a model can have multiple media files like
   images or sounds that shall later be accessed by their file name. To use this
   model simply add a `GenericRelation` to the model that shall have media files.


   .. py:attribute:: content_type


   .. py:attribute:: object_id


   .. py:attribute:: content_object


   .. py:class:: Meta

      Bases: :py:obj:`openbook.core.models.mixins.file.FileUploadMixin.Meta`

      .. autoapi-inheritance-diagram:: openbook.core.models.media_file.MediaFile.Meta
         :parts: 1


      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: ordering
         :value: ['content_type', 'object_id', 'file_name']



      .. py:attribute:: indexes



   .. py:method:: calc_file_path_hook(filename)


