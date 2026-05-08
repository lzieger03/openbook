openbook.auth.models.auth_token
===============================

.. py:module:: openbook.auth.models.auth_token


Attributes
----------

.. autoapisummary::

   openbook.auth.models.auth_token.ALLOWED_CHARACTERS


Classes
-------

.. autoapisummary::

   openbook.auth.models.auth_token.AuthToken


Functions
---------

.. autoapisummary::

   openbook.auth.models.auth_token.generate_token


Module Contents
---------------

.. py:data:: ALLOWED_CHARACTERS
   :value: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


.. py:function:: generate_token(length = 64)

   Generate a new random token string.


.. py:class:: AuthToken

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.core.models.mixins.text.NameDescriptionMixin`, :py:obj:`openbook.core.models.mixins.active.ActiveInactiveMixin`, :py:obj:`openbook.core.models.mixins.datetime.ValidityTimeSpanMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.auth_token.AuthToken
      :parts: 1


   Authentication token that remote clients can use for API authentication. This
   allowed the clients to impersonate the user account associated with the token,
   which can be used in two ways:

   1. As the sole authentication method for app users (technical users).
   2. To authenticate as a human user, instead of a full OAuth resource sharing flow.

   Token life-time can be manually managed by the users.


   .. py:attribute:: user


   .. py:attribute:: token


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: permissions
         :value: (('manage_own_authtoken', 'Can mange own authentication tokens'),)



      .. py:attribute:: indexes



   .. py:method:: has_obj_perm(user_obj, perm)

      Users can only manage their own access key, provided they have the `"openbook_auth.manage_own_authtoken"`
      permission (directly assigned to the user or via user groups, since we don't have a RBAC scope here).

      Note: Users must have the special permission `"openbook_auth.manage_own_authtoken"` in order to manage
      their own tokens. Because assigning the Django default permissions (add, change, delete, view)
      would allow them to manage all tokens of all users (due to the fallback logic in or auth backend).



