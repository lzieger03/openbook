openbook.auth.models.signup_group_assignment
============================================

.. py:module:: openbook.auth.models.signup_group_assignment


Classes
-------

.. autoapisummary::

   openbook.auth.models.signup_group_assignment.SignupGroupAssignment
   openbook.auth.models.signup_group_assignment.SecurityAssertion


Module Contents
---------------

.. py:class:: SignupGroupAssignment

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.active.ActiveInactiveMixin`, :py:obj:`openbook.core.models.mixins.text.NameDescriptionMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.signup_group_assignment.SignupGroupAssignment
      :parts: 1


   Automatic user group assignment after sign-up. For local accounts and most social providers,
   all new users are added to the same user groups. For SAML it is possible to assign different
   groups based on the assertions returned by the IdP.


   .. py:attribute:: site


   .. py:attribute:: social_app


   .. py:attribute:: groups


   .. py:attribute:: is_staff


   .. py:attribute:: is_superuser


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural



   .. py:method:: match(extra_data)

      Check if the given extra data from the social account entry matches all scopes/assertions.



.. py:class:: SecurityAssertion

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.signup_group_assignment.SecurityAssertion
      :parts: 1


   OAuth Scope or SAML Assertion to be checked after sign-up for automatic user
   group assignment.


   .. py:class:: MatchStrategy

      Bases: :py:obj:`django.db.models.TextChoices`

      .. autoapi-inheritance-diagram:: openbook.auth.models.signup_group_assignment.SecurityAssertion.MatchStrategy
         :parts: 1


      Class for creating enumerated string choices.


      .. py:attribute:: EXACT


      .. py:attribute:: CONTAINS


      .. py:attribute:: STARTS_WITH


      .. py:attribute:: ENDS_WITH


      .. py:attribute:: REGEX


      .. py:attribute:: ANY



   .. py:attribute:: parent


   .. py:attribute:: name


   .. py:attribute:: value


   .. py:attribute:: match_strategy


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural



   .. py:method:: match(extra_data)

      Check if the given extra data from the social account entry matches the scope or assertion.



