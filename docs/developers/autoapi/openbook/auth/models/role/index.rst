openbook.auth.models.role
=========================

.. py:module:: openbook.auth.models.role


Classes
-------

.. autoapisummary::

   openbook.auth.models.role.Role


Module Contents
---------------

.. py:class:: Role

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.auth.models.mixins.scope.ScopeMixin`, :py:obj:`openbook.core.models.mixins.slug.NonUniqueSlugMixin`, :py:obj:`openbook.core.models.mixins.text.NameDescriptionMixin`, :py:obj:`openbook.core.models.mixins.active.ActiveInactiveMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.role.Role
      :parts: 1


   Object-based permissions are based on roles that users have in a given context (scope).
   Roles bundle one or more permissions granted to all users assigned to them. For example
   textbooks and courses use roles to restrict who can use them how.


   .. py:attribute:: priority


   .. py:attribute:: permissions


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints


      .. py:attribute:: indexes



