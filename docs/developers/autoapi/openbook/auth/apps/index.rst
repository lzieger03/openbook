openbook.auth.apps
==================

.. py:module:: openbook.auth.apps


Classes
-------

.. autoapisummary::

   openbook.auth.apps.AuthApp


Module Contents
---------------

.. py:class:: AuthApp(app_name, app_module)

   Bases: :py:obj:`django.apps.AppConfig`

   .. autoapi-inheritance-diagram:: openbook.auth.apps.AuthApp
      :parts: 1


   Class representing a Django application and its configuration.


   .. py:attribute:: name
      :value: 'openbook.auth'



   .. py:attribute:: label
      :value: 'openbook_auth'



   .. py:attribute:: verbose_name


   .. py:method:: ready()

      Override this method in subclasses to run code when Django starts.



