openbook.drf.viewsets
=====================

.. py:module:: openbook.drf.viewsets


Attributes
----------

.. autoapisummary::

   openbook.drf.viewsets.OPERATION_ID_SUMMARY


Classes
-------

.. autoapisummary::

   openbook.drf.viewsets.ModelViewSetMixin
   openbook.drf.viewsets.AllowAnonymousListRetrieveViewSetMixin


Functions
---------

.. autoapisummary::

   openbook.drf.viewsets.with_flex_fields_parameters
   openbook.drf.viewsets.add_tag_groups


Module Contents
---------------

.. py:class:: ModelViewSetMixin

   Ensure that object permissions are also checked when creating new model instances.
   DRF checks object permissions on database-loaded objects, but during creation,
   the object doesn't exist yet. Here we validate the input and construct the instance
   before saving to allow permission checks.

   NOTE: This is a mixin that must be used together with `ModelViewSet` to avoid a mysterious
   circular import in DRF. To overwrite the implementation of `post()` the mixin must come first.

   ```python
   class MyViewSet(ModelViewSetMixin, ModelViewSet):
       pass
   ```


   .. py:method:: create(request, *args, **kwargs)


.. py:class:: AllowAnonymousListRetrieveViewSetMixin

   Small view set mixin class that allows unrestricted access to the `list` and `retrieve`
   actions while deferring permission checks for all other actions to the permission classes
   of the view set (usually defined in `settings.py`).


   .. py:method:: get_permissions()


.. py:function:: with_flex_fields_parameters()

   Decorator for view set classes to add the `drf-flex-fields?` query parameters, with which
   clients can choose the fields they want to receive, to the OpenAPI description.


.. py:data:: OPERATION_ID_SUMMARY

.. py:function:: add_tag_groups(result, **kwargs)

   Builds x-tagGroups for drf-spectacular based on OpenAPI extensions:

   - `x-app-name`:   used for tag group
   - `x-model-name`: used as the tag for the endpoint


