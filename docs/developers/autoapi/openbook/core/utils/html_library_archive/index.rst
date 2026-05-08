openbook.core.utils.html_library_archive
========================================

.. py:module:: openbook.core.utils.html_library_archive


Attributes
----------

.. autoapisummary::

   openbook.core.utils.html_library_archive.T


Classes
-------

.. autoapisummary::

   openbook.core.utils.html_library_archive.HTMLLibraryArchive
   openbook.core.utils.html_library_archive.TypedAccessDict
   openbook.core.utils.html_library_archive.HTMLLibraryManifest
   openbook.core.utils.html_library_archive.HTMLComponentManifest
   openbook.core.utils.html_library_archive.HTMLAttributeDescription


Module Contents
---------------

.. py:class:: HTMLLibraryArchive(file, mode = 'r', **zipfile_kwargs)

   Low-level class to work with HTML library archives. Supports checking, if
   an archive is valid, reading its content and extracting it.


   .. py:method:: close()

      Close the archive file when it is not needed anymore. Should always be called
      when done with the archive.



   .. py:method:: is_valid_archive()

      Returns `True` is the archive is a valid HTML library archive. This is, if it
      is a ZIP file, containing a single directory with the name `openbook-library`,
      which in turn contains a `library.yml` file with at least the following content
      with a valid library name and semver version:

      ```yaml
      name: "@organization/name"
      version: 1.0.0
      ```



   .. py:method:: get_library_manifest()

      Returns a python object with the parsed content of the library manifest file.
      Returns `None` when the archive is no ZIP file or lacks the library manifest.



   .. py:method:: get_html_component_manifests()

      Returns a dictionary that maps HTML tag names to python objects that describe
      the HTML custom components. Returns `None` when the archive is no ZIP file.



   .. py:method:: get_raw_zip_file()

      Returns the raw `ZipFile` object so that its content can be inspected. Returns
      `None`, if the file is no valid zip file.



   .. py:method:: extract(install_dir, stdout = sys.stdout, verbosity = 0)

      Extract archive content into the given installation directory. The directory should be
      the root directory where all libraries are installed, because this method will create
      the corresponding sub-directories for the library and its version. If a sub-directory
      for the same version of the same library already exists it will be deleted first.

      Note, no validation of the archive is done here. It is assumed that the client already
      called `is_valid_archive()` or wants to force-extract a possibly invalid archive.

      Does nothing if the archive is no ZIP file.

      :param install_dir: Root directory where libraries are installed
      :param stdout: Output stream for console messages
      :param verbosity: Print details on the console (default: 0 = off)



.. py:data:: T

.. py:class:: TypedAccessDict(data)

   Bases: :py:obj:`dict`

   .. autoapi-inheritance-diagram:: openbook.core.utils.html_library_archive.TypedAccessDict
      :parts: 1


   Specialized dictionary that can apply runtime type checking when accessing
   its content. This is used for parsing the manifest files of a HTML library
   archive to make sure that values with unexpected types will be skipped.

   Nested dictionaries will automatically converted into typed dictionaries,
   to allow type-checking their content, too. Still the expected type must
   be given as `dict`.


   .. py:method:: get_typed(key, expected_type, default_value = None)

      Dictionary access with type checking.

      :param key: Key name
      :param expected_type: Type to be checked with `isinstance()`
      :param default_value: Default value if key is missing or value has wrong type



   .. py:method:: get_string_list(key)

      Access a list of strings in the dictionary with runtime type-checking.



   .. py:method:: get_string_dict(key)

      Access a raw dictionary whose keys and values are both strings.



.. py:class:: HTMLLibraryManifest(organization = '', name = '', version = '', author = '', license = '', website = '', coderepo = '', bugtracker = '', description = {}, readme = '', dependencies = {})

   Content of the `library.yml` file that describes the library as a whole.


   .. py:attribute:: organization
      :value: ''



   .. py:attribute:: name
      :value: ''



   .. py:attribute:: version
      :value: ''



   .. py:attribute:: author
      :value: ''



   .. py:attribute:: license
      :value: ''



   .. py:attribute:: website
      :value: ''



   .. py:attribute:: coderepo
      :value: ''



   .. py:attribute:: bugtracker
      :value: ''



   .. py:attribute:: description


   .. py:attribute:: readme
      :value: ''



   .. py:attribute:: dependencies


   .. py:method:: from_dict(manifest_data)
      :classmethod:


      Create new instance from a dictionary in the YAML manifest file.



.. py:class:: HTMLComponentManifest(tag_name = '', description = {}, text_allowed = False, html_allowed = False, allowed_children = [], attributes = {}, events = [])

   Content of a component YAML file describing a single HTML custom component.


   .. py:attribute:: tag_name
      :value: ''



   .. py:attribute:: description


   .. py:attribute:: text_allowed
      :value: False



   .. py:attribute:: html_allowed
      :value: False



   .. py:attribute:: allowed_children
      :value: []



   .. py:attribute:: attributes


   .. py:attribute:: events
      :value: []



   .. py:method:: from_dict(manifest_data)
      :classmethod:


      Create new instance from a dictionary in the YAML manifest file.



   .. py:method:: to_dict()


.. py:class:: HTMLAttributeDescription(name = '', description = {}, regex = '', enum = [])

   Description of a HTML attribute.


   .. py:attribute:: name
      :value: ''



   .. py:attribute:: description


   .. py:attribute:: regex
      :value: ''



   .. py:attribute:: enum
      :value: []



   .. py:method:: from_dict(attribute_name, attribute_data)
      :classmethod:



   .. py:method:: to_dict()


