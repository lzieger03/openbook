openbook.auth.middleware.current_user
=====================================

.. py:module:: openbook.auth.middleware.current_user


Attributes
----------

.. autoapisummary::

   openbook.auth.middleware.current_user.thread_local


Classes
-------

.. autoapisummary::

   openbook.auth.middleware.current_user.CurrentUserTrackingAuthentication
   openbook.auth.middleware.current_user.CurrentUserTrackingAuthExtension


Functions
---------

.. autoapisummary::

   openbook.auth.middleware.current_user.CurrentUserMiddleware
   openbook.auth.middleware.current_user.get_current_user
   openbook.auth.middleware.current_user.reset_current_user


Module Contents
---------------

.. py:data:: thread_local

.. py:function:: CurrentUserMiddleware(get_response)

   Save the current user in a thread-local variable so that it can be accessed
   within the model layer. This is done to auto-populate the `created_by` and
   `modified_by` fields of models that use the `CreatedModifiedByMixin` without
   needing to explicitly pass the user from the view layer to the model layer.


.. py:class:: CurrentUserTrackingAuthentication

   Bases: :py:obj:`rest_framework.authentication.BaseAuthentication`

   .. autoapi-inheritance-diagram:: openbook.auth.middleware.current_user.CurrentUserTrackingAuthentication
      :parts: 1


   The same as above but for Django REST Framework, which wraps the plain Django
   request object and resolves the user only when first accessed. Because of this
   the middleware above only sees the initial anonymous user.


   .. py:attribute:: auth_classes
      :value: []



   .. py:method:: authenticate(request)

      Authenticate the request and return a two-tuple of (user, token).



.. py:function:: get_current_user()

   Get the current request user, if any. Returns `None` otherwise.


.. py:function:: reset_current_user()

   Needed for unit tests which all run in a single thread. Forget previous tests's
   user as it is probably not even existing anymore.


.. py:class:: CurrentUserTrackingAuthExtension(target)

   Bases: :py:obj:`drf_spectacular.extensions.OpenApiAuthenticationExtension`

   .. autoapi-inheritance-diagram:: openbook.auth.middleware.current_user.CurrentUserTrackingAuthExtension
      :parts: 1


   To resolve the following warning: "could not resolve authenticator
   <class 'openbook.auth.middleware.current_user.CurrentUserTrackingAuthentication'>.
   There was no OpenApiAuthenticationExtension registered for that class.
   Try creating one by subclassing it. Ignoring for now."

   As it is defined, we are using session authentication despite our custom
   permission class (wich doesn't affect authentication at all)


   .. py:attribute:: target_class


   .. py:attribute:: name
      :value: 'SessionAuthentication'



   .. py:method:: get_security_definition(auto_schema)


