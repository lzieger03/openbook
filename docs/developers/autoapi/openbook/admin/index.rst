openbook.admin
==============

.. py:module:: openbook.admin


Attributes
----------

.. autoapisummary::

   openbook.admin.admin_site


Classes
-------

.. autoapisummary::

   openbook.admin.ImportExportModelResource
   openbook.admin.CustomModelAdmin
   openbook.admin.CustomAdminSite


Module Contents
---------------

.. py:class:: ImportExportModelResource(**kwargs)

   Bases: :py:obj:`import_export.resources.ModelResource`

   .. autoapi-inheritance-diagram:: openbook.admin.ImportExportModelResource
      :parts: 1


   Custom `ModelResource` that allows to delete entries when importing model data
   in the Admin from CSV, YML, XLSX, … files. For this the files may include a row
   called `delete` with a boolean value to indicate the rows to be deleted.


   .. py:attribute:: delete


   .. py:method:: dehydrate_delete(obj)


   .. py:method:: for_delete(row, instance)

      Returns ``True`` if ``row`` importing should delete instance.

      Default implementation returns ``False``.
      Override this method to handle deletion.

      :param row: A ``dict`` containing key / value data for the row to be imported.

      :param instance: A new or existing model instance.



.. py:class:: CustomModelAdmin(model, admin_site)

   Bases: :py:obj:`djangoql.admin.DjangoQLSearchMixin`, :py:obj:`unfold.admin.ModelAdmin`, :py:obj:`import_export.admin.ImportExportModelAdmin`

   .. autoapi-inheritance-diagram:: openbook.admin.CustomModelAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: save_as
      :value: True



   .. py:attribute:: warn_unsaved_form
      :value: True



   .. py:attribute:: compressed_fields
      :value: True



.. py:class:: CustomAdminSite

   Bases: :py:obj:`unfold.sites.UnfoldAdminSite`

   .. autoapi-inheritance-diagram:: openbook.admin.CustomAdminSite
      :parts: 1


   Custom `AdminSite` class that allows us to override the default alphabetical
   order of apps and models on the dashboard. Instead apps will be sorted in the
   order they are listed in `settings.INSTALLED_APPS`. And models will be sorted
   in the order they are registered with the admin site.


   .. py:method:: register(model_or_iterable, admin_class, **options)

      Hook into Django Admin's `register()` method to remember the order in which
      the models were registered.



   .. py:method:: unregister(model_or_iterable)

      Hook into Django Admin's `unregister()` method to remove a model from the
      internal list.



   .. py:method:: get_app_list(request, *args)

      Hook into Django Admin's `get_app_list()` method to override the order in
      which the applications and models appear.



.. py:data:: admin_site

