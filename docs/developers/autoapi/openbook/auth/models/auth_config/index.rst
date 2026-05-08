openbook.auth.models.auth_config
================================

.. py:module:: openbook.auth.models.auth_config


Classes
-------

.. autoapisummary::

   openbook.auth.models.auth_config.AuthConfig
   openbook.auth.models.auth_config.AuthConfigText


Module Contents
---------------

.. py:class:: AuthConfig(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.auth.models.auth_config.AuthConfig
      :parts: 1


   Authentication related configuration for the site.


   .. py:attribute:: site


   .. py:attribute:: local_signup_allowed


   .. py:attribute:: signup_email_suffix


   .. py:attribute:: logout_next_url


   .. py:attribute:: signup_image


   .. py:attribute:: login_image


   .. py:attribute:: logout_image


   .. py:attribute:: password_reset_image


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural



   .. py:method:: get_for_default_site()
      :classmethod:


      Get authorization configuration for the default site defined in the `SITE_ID`
      Django settings. Raises `AuthConfig.DoesNotExist`, if not found.



.. py:class:: AuthConfigText

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.i18n.TranslatableMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.auth_config.AuthConfigText
      :parts: 1


   .. py:attribute:: parent


   .. py:attribute:: logout_next_text


   .. py:class:: Meta

      Bases: :py:obj:`openbook.core.models.mixins.i18n.TranslatableMixin.Meta`

      .. autoapi-inheritance-diagram:: openbook.auth.models.auth_config.AuthConfigText.Meta
         :parts: 1


      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: constraints



