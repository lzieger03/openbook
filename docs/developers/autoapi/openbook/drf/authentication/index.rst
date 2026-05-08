openbook.drf.authentication
===========================

.. py:module:: openbook.drf.authentication


Classes
-------

.. autoapisummary::

   openbook.drf.authentication.TokenAuthentication


Module Contents
---------------

.. py:class:: TokenAuthentication

   Bases: :py:obj:`rest_framework.authentication.BaseAuthentication`

   .. autoapi-inheritance-diagram:: openbook.drf.authentication.TokenAuthentication
      :parts: 1


   Token authentication for app users. Works hand in hand with the `AuthToken` model
   in the `openbook_auth` app. Based on the class `TokenAuthentication` in DRF.


   .. py:attribute:: keyword
      :value: 'Token'



   .. py:method:: authenticate(request)

      Authenticate the request and return a two-tuple of `(user, token)` or `None`.



   .. py:method:: authenticate_header(request)

      Return string to be used as the value of the `WWW-Authenticate` header in a
      `401 Unauthenticated` response.



