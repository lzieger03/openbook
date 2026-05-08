openbook.auth.filters.mixins.audit
==================================

.. py:module:: openbook.auth.filters.mixins.audit


Classes
-------

.. autoapisummary::

   openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin


Module Contents
---------------

.. py:class:: CreatedModifiedByFilterMixin(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin
      :parts: 1


   Mixin filter class for any model that implements the `CreatedModifiedByMixin` and has the
   `created_by`, `created_at`, `modified_by` and `modified_at` fields.


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: fields



   .. py:method:: created_by_filter(queryset, name, value)


   .. py:method:: modified_by_filter(queryset, name, value)


