openbook.drf.filters
====================

.. py:module:: openbook.drf.filters


Classes
-------

.. autoapisummary::

   openbook.drf.filters.DjangoObjectPermissionsFilter


Module Contents
---------------

.. py:class:: DjangoObjectPermissionsFilter

   Bases: :py:obj:`rest_framework.filters.BaseFilterBackend`

   .. autoapi-inheritance-diagram:: openbook.drf.filters.DjangoObjectPermissionsFilter
      :parts: 1


   Filter implementation inspired by `django-rest-framework-guardian2` `ObjectPermissionsFilter`.
   Filters out all objects from a queryset for which the user has no object-level view permission.


   .. py:method:: filter_queryset(request, queryset, view)

      Return a filtered queryset.



