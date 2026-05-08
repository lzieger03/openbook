openbook.core.middleware.current_language
=========================================

.. py:module:: openbook.core.middleware.current_language


Attributes
----------

.. autoapisummary::

   openbook.core.middleware.current_language.thread_local


Functions
---------

.. autoapisummary::

   openbook.core.middleware.current_language.CurrentLanguageMiddleware
   openbook.core.middleware.current_language.get_current_language


Module Contents
---------------

.. py:data:: thread_local

.. py:function:: CurrentLanguageMiddleware(get_response)

   Save the current language in a thread-local variable so that it can be accessed
   within the other layers. This is done to get the language in DRF serializers that
   needs to handle translation themselves.


.. py:function:: get_current_language()

   Get the current request language, if any. Returns `None` otherwise.


