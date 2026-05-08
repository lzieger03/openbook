openbook.core.models.mixins.slug
================================

.. py:module:: openbook.core.models.mixins.slug


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.slug.NonUniqueSlugMixin
   openbook.core.models.mixins.slug.UniqueSlugMixin


Module Contents
---------------

.. py:class:: NonUniqueSlugMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.slug.NonUniqueSlugMixin
      :parts: 1


   Mixin for models with a non-unique slug field. This is usually used, if the slug
   itself cannot be unique but must be unique in combination with other fields. In
   that case, the child class can define a constraint like so:

   ```python
   class MyModel(models.Model, NonUniqueSlugMixin):
       ...
       class Meta:
           constraints = (
               models.UniqueConstraint(fields=("course", "slug"), name="unique_course_slug"),
           )
   ```


   .. py:attribute:: slug


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




.. py:class:: UniqueSlugMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.slug.UniqueSlugMixin
      :parts: 1


   Mixin for models with a unique slug field.


   .. py:attribute:: slug


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




