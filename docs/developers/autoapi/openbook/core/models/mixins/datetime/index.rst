openbook.core.models.mixins.datetime
====================================

.. py:module:: openbook.core.models.mixins.datetime


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.datetime.ValidityTimeSpanMixin
   openbook.core.models.mixins.datetime.DurationMixin


Module Contents
---------------

.. py:class:: ValidityTimeSpanMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.datetime.ValidityTimeSpanMixin
      :parts: 1


   Mixin class for models that have a validity optionally starting at a certain point
   in time and optionally ending at a later point in time.


   .. py:attribute:: start_date


   .. py:attribute:: end_date


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:method:: clean()

      Custom check when the model is saved that the end date must be later then the
      start date, if both respective flags are set. If one of the two flags is unset
      the check will be skipped.

      Care must be taken to call this method, if the `clean()` method is overwritten by another
      mixin class or the model itself.



   .. py:property:: validity_time_span

      Get formatted string to display in the Admin or on the website.


.. py:class:: DurationMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.datetime.DurationMixin
      :parts: 1


   Mixin class for models that have a duration in minutes, hours, days, weeks, months or years.


   .. py:class:: DurationPeriod

      Bases: :py:obj:`django.db.models.TextChoices`

      .. autoapi-inheritance-diagram:: openbook.core.models.mixins.datetime.DurationMixin.DurationPeriod
         :parts: 1


      Class for creating enumerated string choices.


      .. py:attribute:: MINUTES


      .. py:attribute:: HOURS


      .. py:attribute:: DAYS


      .. py:attribute:: WEEKS


      .. py:attribute:: MONTHS


      .. py:attribute:: YEARS



   .. py:attribute:: duration_period


   .. py:attribute:: duration_value


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True




   .. py:property:: duration

      Get formatted string to display in the Admin or on the website.


   .. py:method:: save(*args, **kwargs)

      Make sure to not fail the NOT NULL constraint on duration value.



   .. py:method:: add_duration_to(timestamp)

      Add the specified duration to the given timestamp.



