openbook.core.apps
==================

.. py:module:: openbook.core.apps


Classes
-------

.. autoapisummary::

   openbook.core.apps.OpenBookServerApp


Module Contents
---------------

.. py:class:: OpenBookServerApp(app_name, app_module)

   Bases: :py:obj:`django.apps.AppConfig`

   .. autoapi-inheritance-diagram:: openbook.core.apps.OpenBookServerApp
      :parts: 1


   Class representing a Django application and its configuration.


   .. py:attribute:: name
      :value: 'openbook.core'



   .. py:attribute:: label
      :value: 'openbook_core'



   .. py:attribute:: verbose_name


   .. py:method:: ready()

      Patch `ContentType.__str__` to return the model only, without prefixing it
      with the app name.



