openbook.auth.models.access_request
===================================

.. py:module:: openbook.auth.models.access_request


Classes
-------

.. autoapisummary::

   openbook.auth.models.access_request.AccessRequest


Module Contents
---------------

.. py:class:: AccessRequest

   Bases: :py:obj:`openbook.core.models.mixins.uuid.UUIDMixin`, :py:obj:`openbook.auth.models.mixins.scope.ScopeMixin`, :py:obj:`openbook.core.models.mixins.datetime.DurationMixin`, :py:obj:`openbook.auth.models.mixins.audit.CreatedModifiedByMixin`

   .. autoapi-inheritance-diagram:: openbook.auth.models.access_request.AccessRequest
      :parts: 1


   To gain access, users may send access requests to the owners of a given scope. This contains the
   scope and the requested role, so that the request can be converted into a role assignment, if the
   request is granted.

   NOTE: Take care to exclude `decision` and `decision_date` when creating and modifying objects.


   .. py:class:: Decision

      Bases: :py:obj:`django.db.models.TextChoices`

      .. autoapi-inheritance-diagram:: openbook.auth.models.access_request.AccessRequest.Decision
         :parts: 1


      Class for creating enumerated string choices.


      .. py:attribute:: PENDING


      .. py:attribute:: ACCEPTED


      .. py:attribute:: DENIED



   .. py:attribute:: user


   .. py:attribute:: role


   .. py:attribute:: end_date


   .. py:attribute:: decision


   .. py:attribute:: decision_date


   .. py:class:: Meta

      .. py:attribute:: verbose_name


      .. py:attribute:: verbose_name_plural


      .. py:attribute:: indexes



   .. py:method:: has_obj_perm(user_obj, perm)

      Always allow to view or delete own access requests, as well as to create new pending requests for
      the own user. Otherwise use inherited object permission, that the target role's priority must be
      lower or equal any priority of the own assigned roles.



   .. py:method:: save(*args, **kwargs)

      Force pending decision when a new access request is saved. Also update the role assignments
      accordingly when a decision is made.



   .. py:method:: accept(permission_user = None, check_permission = True)

      Accept request by setting the decision to accepted, saving the object and creating
      the role assignment.



   .. py:method:: deny(permission_user = None, check_permission = True)

      Deny access request by setting the decision to denied and saving the object.



