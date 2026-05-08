openbook.core.models.html_component
===================================

.. py:module:: openbook.core.models.html_component


Classes
-------

.. autoapisummary::

   openbook.core.models.html_component.HTMLComponent
   openbook.core.models.html_component.HTMLComponentDefinition


Module Contents
---------------

.. py:class:: HTMLComponent

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`

   .. autoapi-inheritance-diagram:: openbook.core.models.html_component.HTMLComponent
      :parts: 1


   HTML custom component defined in a HTML library. This model makes the custom elements known to
   the WYSIWYG editor.


   .. py:attribute:: library


   .. py:attribute:: tag_name


   .. py:method:: min_version()


   .. py:method:: max_version()


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints



   .. py:method:: get_by_tag_name(library_fqn, tag_name)
      :classmethod:



.. py:class:: HTMLComponentDefinition

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`

   .. autoapi-inheritance-diagram:: openbook.core.models.html_component.HTMLComponentDefinition
      :parts: 1


   Version dependent definition of a HTML component, containing a JSON manifest to be used by the
   WYSIWYG editor.


   .. py:attribute:: html_component


   .. py:attribute:: library_version


   .. py:attribute:: definition


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints



   .. py:method:: library_version_version()


   .. py:method:: library_version_created_by()


   .. py:method:: library_version_created_at()


   .. py:method:: library_version_modified_by()


   .. py:method:: library_version_modified_at()


   .. py:method:: clean()

      Validate that HTML component and library version refer to the same library.



