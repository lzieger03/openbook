openbook.auth.viewsets.auth_config
==================================

.. py:module:: openbook.auth.viewsets.auth_config


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.auth_config.AuthConfigTextSerializer
   openbook.auth.viewsets.auth_config.AuthConfigSerializer


Module Contents
---------------

.. py:class:: AuthConfigTextSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.auth_config.AuthConfigTextSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['parent', 'language', 'logout_next_text']



      .. py:attribute:: expandable_fields



.. py:class:: AuthConfigSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.auth_config.AuthConfigSerializer
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['site', 'local_signup_allowed', 'signup_email_suffix', 'logout_next_url', 'signup_image',...



      .. py:attribute:: expandable_fields



