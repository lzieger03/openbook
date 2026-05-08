openbook.core.admin.site
========================

.. py:module:: openbook.core.admin.site


Classes
-------

.. autoapisummary::

   openbook.core.admin.site.SiteResource
   openbook.core.admin.site.SiteAdmin


Module Contents
---------------

.. py:class:: SiteResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.site.SiteResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'delete', 'domain', 'name', 'short_name', 'about_url', 'brand_color']




.. py:class:: SiteAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.core.admin.site.SiteAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ['id', 'domain', 'name', 'short_name']



   .. py:attribute:: list_display_links
      :value: ['id', 'domain']



   .. py:attribute:: search_fields
      :value: ['domain', 'name', 'short_name']



   .. py:attribute:: fieldsets


