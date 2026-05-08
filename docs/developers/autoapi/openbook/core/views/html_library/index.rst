openbook.core.views.html_library
================================

.. py:module:: openbook.core.views.html_library


Classes
-------

.. autoapisummary::

   openbook.core.views.html_library.UnpackHTMLLibraryArchivesForm
   openbook.core.views.html_library.UnpackHTMLLibraryArchivesView


Module Contents
---------------

.. py:class:: UnpackHTMLLibraryArchivesForm(data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None, renderer=None, bound_field_class=None)

   Bases: :py:obj:`django.forms.Form`

   .. autoapi-inheritance-diagram:: openbook.core.views.html_library.UnpackHTMLLibraryArchivesForm
      :parts: 1


   Custom form to render the input fields with proper styling.


   .. py:attribute:: library_versions


   .. py:attribute:: extract_archive


   .. py:attribute:: update_library


   .. py:attribute:: update_version


   .. py:attribute:: update_components


   .. py:attribute:: verbosity


   .. py:method:: set_library(library)


.. py:class:: UnpackHTMLLibraryArchivesView(model_admin, **kwargs)

   Bases: :py:obj:`unfold.views.UnfoldModelAdminViewMixin`, :py:obj:`django.views.generic.FormView`

   .. autoapi-inheritance-diagram:: openbook.core.views.html_library.UnpackHTMLLibraryArchivesView
      :parts: 1


   Custom view that allows to unpack uploaded library archives in the Django Admin.
   The view is called for a single library of which the versions can be selected
   whose archives shall be unpacked and further installed.


   .. py:attribute:: title


   .. py:attribute:: permission_required
      :value: ['openbook_core.change_htmllibraryversion']



   .. py:attribute:: template_name
      :value: 'openbook_core/admin/html_library/unpack.html'



   .. py:attribute:: form_class


   .. py:method:: setup(request, *args, library_id, **kwargs)

      Setup view instance. Read library from database.



   .. py:method:: get_context_data(**kwargs)

      Populate template context for rendering the output page.



   .. py:method:: get_form(form_class=None)

      Initialize form and pass the library so that the library version choices can be set.



   .. py:method:: form_valid(form)

      Process valid form data by calling the installation method with the arguments received
      from the form. Unlike normal form handling, don't redirect but simply render the form
      again, so that the transient log output can be shown.



