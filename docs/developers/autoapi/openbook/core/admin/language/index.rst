openbook.core.admin.language
============================

.. py:module:: openbook.core.admin.language


Classes
-------

.. autoapisummary::

   openbook.core.admin.language.LanguageResource
   openbook.core.admin.language.LanguageAdmin


Module Contents
---------------

.. py:class:: LanguageResource(**kwargs)

   Bases: :py:obj:`openbook.admin.ImportExportModelResource`

   .. autoapi-inheritance-diagram:: openbook.core.admin.language.LanguageResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: import_id_fields
         :value: ('language',)



      .. py:attribute:: fields
         :value: ('language', 'delete', 'name')




.. py:class:: LanguageAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.core.admin.language.LanguageAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: model


   .. py:attribute:: resource_classes


   .. py:attribute:: list_display
      :value: ('language', 'name')



   .. py:attribute:: list_display_links
      :value: ('language', 'name')



   .. py:attribute:: search_fields
      :value: ('language', 'name')



   .. py:attribute:: fields
      :value: ('language', 'name')



