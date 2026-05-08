openbook.auth.models.enrollment_method
======================================

.. py:module:: openbook.auth.models.enrollment_method


Classes
-------

.. autoapisummary::

   openbook.auth.models.enrollment_method.EnrollmentMethod


Module Contents
---------------

.. py:class:: EnrollmentMethod

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.auth.models.mixins.scope.ScopeMixin`, :py:obj:`openbook.core.models.mixins.text.NameDescriptionMixin`, :py:obj:`openbook.core.models.mixins.active.ActiveInactiveMixin`, :py:obj:`openbook.core.models.mixins.datetime.DurationMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.enrollment_method.EnrollmentMethod
      :parts: 1


   Enrollment methods all users to enroll themselves to get access. Enrollment is always bound to
   a role that will be assigned to the users and can optionally have a limited duration. Also the
   enrollment can be protected with a passphrase, that users must enter.

   NOTE: Take care to not reveal the passphrase when enrollment methods are queried or viewed.


   .. py:attribute:: role


   .. py:attribute:: end_date


   .. py:attribute:: passphrase


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: indexes


      .. py:attribute:: permissions
         :value: (('self_enroll', 'Can self-enroll in a scope'),)




   .. py:method:: enroll(user, passphrase = None, check_passphrase = True, check_permission = True)

      Enroll the given user, optionally checking the passphrase. Raises a `ValueError` when
      the passphrase doesn't match.



