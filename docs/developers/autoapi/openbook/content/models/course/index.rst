openbook.content.models.course
==============================

.. py:module:: openbook.content.models.course


Classes
-------

.. autoapisummary::

   openbook.content.models.course.Course


Module Contents
---------------

.. py:class:: Course(*args, **kwargs)

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.slug.NonUniqueSlugMixin`, :py:obj:`openbook.core.models.mixins.text.NameDescriptionMixin`, :py:obj:`openbook.auth.models.mixins.scope.ScopedRolesMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.content.models.course.Course
      :parts: 1


   Courses support the teachers in the execution of the teaching by bringing together teachers,
   students, textbooks and other one-off materials.


   .. py:attribute:: is_template


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural



