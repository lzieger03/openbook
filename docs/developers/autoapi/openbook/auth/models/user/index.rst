openbook.auth.models.user
=========================

.. py:module:: openbook.auth.models.user


Classes
-------

.. autoapisummary::

   openbook.auth.models.user.User


Module Contents
---------------

.. py:class:: User(*args, **kwargs)

   Bases: :py:obj:`django.contrib.auth.models.AbstractUser`

   .. autoapi-inheritance-diagram:: openbook.auth.models.user.User
      :parts: 1


   Extension to Django's core user model to distinguish different user types and add
   some user profile fields.


   .. py:class:: UserType

      Bases: :py:obj:`django.db.models.TextChoices`

      .. autoapi-inheritance-diagram:: openbook.auth.models.user.User.UserType
         :parts: 1


      Class for creating enumerated string choices.


      .. py:attribute:: HUMAN


      .. py:attribute:: APP



   .. py:attribute:: user_type


   .. py:attribute:: email


   .. py:attribute:: description


   .. py:attribute:: picture


   .. py:attribute:: groups


   .. py:method:: full_name(obj=None)

      Name, e-mail and profile picture. Note that Django Unfold only supports this in the
      changelist not on the detail page.



   .. py:method:: has_obj_perm(user_obj, perm)

      Allow users to update and delete their account.



