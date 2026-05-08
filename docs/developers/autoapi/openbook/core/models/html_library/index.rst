openbook.core.models.html_library
=================================

.. py:module:: openbook.core.models.html_library


Classes
-------

.. autoapisummary::

   openbook.core.models.html_library.HTMLLibrary
   openbook.core.models.html_library.HTMLLibraryText
   openbook.core.models.html_library.HTMLLibraryVersion


Module Contents
---------------

.. py:class:: HTMLLibrary(*args, **kwargs)

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.core.models.html_library.HTMLLibrary
      :parts: 1


   Textbooks are basically static HTML pages that embed the OpenBook JavaScript libraries to render
   custom components (web components). Those web components might in turn communicate with the server
   if necessary, but usually are working stand-alone. For this the distribution bundle needs to be
   loaded via the corresponding `<script>` and `<link rel="stylesheet">` tags.

   To make a library available to the server and especially the WYSIWYG editor, it must be "installed"
   on the server. This includes creating a few database entries (of which this is the main one) and
   placing the bundled library code in the directory `MEDIA_DIR/lib/{organization}/{library}/{version}`.


   .. py:attribute:: organization


   .. py:attribute:: name


   .. py:attribute:: author


   .. py:attribute:: license


   .. py:attribute:: website


   .. py:attribute:: coderepo


   .. py:attribute:: bugtracker


   .. py:attribute:: readme


   .. py:attribute:: text_format


   .. py:attribute:: published


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints



   .. py:method:: fqn()


   .. py:method:: get_by_fqn(fqn)
      :classmethod:



   .. py:method:: install_archive(archive_file, extract_archive = True, update_library = True, update_version = True, update_components = True, library_version = None, stdout = sys.stdout, verbosity = 0)
      :classmethod:


      Static method to install a new library version from a library archive file. Depending on
      the flags, only the archive will be extracted or the database entries will also be updated.
      Missing database entries will then be created, already existing entries will be updated.

      :param archive_file: `File` object  for the library archive (usually inside `MEDIA/lib`)
      :param extract_archive: Extract archive file on filesystem
      :param update_library: Update header data of the library
      :param update_version: Update library version data
      :param update_components: Update HTML component definitions
      :param library_version: Skip database lookup and update this library and version entries, instead,
      :param stdout: Output stream for console messages
      :param verbosity: Print details on the console (default: 0 = off)



.. py:class:: HTMLLibraryText

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.i18n.TranslatableMixin`

   .. autoapi-inheritance-diagram:: openbook.core.models.html_library.HTMLLibraryText
      :parts: 1


   .. py:attribute:: parent


   .. py:attribute:: short_description


   .. py:class:: Meta

      Bases: :py:obj:`openbook.core.models.mixins.i18n.TranslatableMixin.Meta`

      .. autoapi-inheritance-diagram:: openbook.core.models.html_library.HTMLLibraryText.Meta
         :parts: 1


      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural



.. py:class:: HTMLLibraryVersion(*args, **kwargs)

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.file.FileUploadMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.core.models.html_library.HTMLLibraryVersion
      :parts: 1


   Mixin class for models that shall record the time and user of creation as well as
   the time and user of the last modification.


   .. py:attribute:: parent


   .. py:attribute:: version


   .. py:attribute:: dependencies


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints


      .. py:attribute:: ordering
         :value: ['parent', '-version']




   .. py:method:: fqn()


   .. py:method:: frontend_url()


   .. py:method:: get_by_fqn(fqn)
      :classmethod:



   .. py:method:: get_by_library_version(library, version)
      :classmethod:



   .. py:method:: calc_file_path_hook(filename)


   .. py:method:: unpack_archive(extract_archive = True, update_library = True, update_version = True, update_components = True, stdout = sys.stdout, verbosity = 0)

      Unpack the archive uploaded to this HTML library version and optionally use the manifest
      data inside the archive to update the database entries.

      :param extract_archive: Extract archive file on filesystem
      :param update_library: Update header data of the library
      :param update_version: Update data of this library version
      :param update_components: Update HTML component definitions
      :param stdout: Output stream for console messages
      :param verbosity: Print details on the console (default: 0 = off)

      :raises ObjectDoesNotExist: No archive file attached to this entry



