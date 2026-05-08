openbook.auth.models.group
==========================

.. py:module:: openbook.auth.models.group


Classes
-------

.. autoapisummary::

   openbook.auth.models.group.Group


Module Contents
---------------

.. py:class:: Group(*args, **kwargs)

   Bases: :py:obj:`openbook.core.models.mixins.slug.UniqueSlugMixin`, :py:obj:`django.contrib.auth.models.Group`

   .. autoapi-inheritance-diagram:: openbook.auth.models.group.Group
      :parts: 1


   Dummy class to move the Group model from `django.contrib.auth` into our own app,
   so that users and groups stand together in the Admin.


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural



   .. py:method:: user_count()


