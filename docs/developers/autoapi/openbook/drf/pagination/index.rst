openbook.drf.pagination
=======================

.. py:module:: openbook.drf.pagination


Classes
-------

.. autoapisummary::

   openbook.drf.pagination.PageNumberPagination


Module Contents
---------------

.. py:class:: PageNumberPagination

   Bases: :py:obj:`rest_framework.pagination.PageNumberPagination`

   .. autoapi-inheritance-diagram:: openbook.drf.pagination.PageNumberPagination
      :parts: 1


   Custom pagination class that allows changing the query parameters used for pagination
   in the Django config, following the same style the DRF uses for the filter backends.


   .. py:attribute:: page_query_param


   .. py:attribute:: page_size_query_param


