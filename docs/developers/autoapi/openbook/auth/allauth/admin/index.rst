openbook.auth.allauth.admin
===========================

.. py:module:: openbook.auth.allauth.admin


Classes
-------

.. autoapisummary::

   openbook.auth.allauth.admin.EmailAddressAdmin
   openbook.auth.allauth.admin.EmailConfirmationAdmin
   openbook.auth.allauth.admin.SocialAppForm
   openbook.auth.allauth.admin.SocialAppAdmin
   openbook.auth.allauth.admin.SocialAccountAdmin
   openbook.auth.allauth.admin.SocialTokenAdmin


Module Contents
---------------

.. py:class:: EmailAddressAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`, :py:obj:`allauth.account.admin.EmailAddressAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.EmailAddressAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


.. py:class:: EmailConfirmationAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`, :py:obj:`allauth.account.admin.EmailConfirmationAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.EmailConfirmationAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


.. py:class:: SocialAppForm(*args, **kwargs)

   Bases: :py:obj:`allauth.socialaccount.admin.SocialAppForm`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.SocialAppForm
      :parts: 1


   The main implementation of all the Form logic. Note that this class is
   different than Form. See the comments by the Form class for more info. Any
   improvements to the form API should be made to this class, not to the Form
   class.


   .. py:class:: Meta

      Bases: :py:obj:`allauth.socialaccount.admin.SocialAppForm.Meta`

      .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.SocialAppForm.Meta
         :parts: 1


      .. py:attribute:: widgets



.. py:class:: SocialAppAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`, :py:obj:`allauth.socialaccount.admin.SocialAppAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.SocialAppAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


   .. py:attribute:: form


.. py:class:: SocialAccountAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`, :py:obj:`allauth.socialaccount.admin.SocialAccountAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.SocialAccountAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


.. py:class:: SocialTokenAdmin(model, admin_site)

   Bases: :py:obj:`openbook.admin.CustomModelAdmin`, :py:obj:`allauth.socialaccount.admin.SocialTokenAdmin`

   .. autoapi-inheritance-diagram:: openbook.auth.allauth.admin.SocialTokenAdmin
      :parts: 1


   Custom `ModelAdmin` to combines several mixins from Django Unfold, Django QL and
   Django Import/Export into on common base-class.


