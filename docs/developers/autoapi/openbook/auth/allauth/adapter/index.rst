openbook.auth.allauth.adapter
=============================

.. py:module:: openbook.auth.allauth.adapter


Classes
-------

.. autoapisummary::

   openbook.auth.allauth.adapter.AccountAdapter
   openbook.auth.allauth.adapter.SocialAccountAdapter


Module Contents
---------------

.. py:class:: AccountAdapter(request = None)

   Bases: :py:obj:`allauth.account.adapter.DefaultAccountAdapter`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.adapter.AccountAdapter
      :parts: 1


   Adapted behavior for local account registration.


   .. py:method:: is_open_for_signup(request)

      Check whether local account registration is allowed.



   .. py:method:: clean_email(email)

      Restrict local account e-mail to e-mails with a certain suffix.



   .. py:method:: save_user(request, user, form, commit=True)

      Add user to groups after sign-up.



   .. py:method:: authenticate(request, **credentials)

      Only allow human users to authenticate. App users need to authenticate with an
      authentication token, instead. This is an extra security measure, since normally
      app users should not have a passwort set and thus should not be able to login
      with username/password, anyway.



.. py:class:: SocialAccountAdapter(request = None)

   Bases: :py:obj:`allauth.socialaccount.adapter.DefaultSocialAccountAdapter`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.adapter.SocialAccountAdapter
      :parts: 1


   Adapted behavior for social account registration.


   .. py:method:: save_user(request, sociallogin, form=None)

      Add user to groups after sign-up.



