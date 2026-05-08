openbook.auth.viewsets.auth_token
=================================

.. py:module:: openbook.auth.viewsets.auth_token


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.auth_token.AuthTokenSerializer
   openbook.auth.viewsets.auth_token.AuthTokenUpdateSerializer
   openbook.auth.viewsets.auth_token.AuthTokenFilter
   openbook.auth.viewsets.auth_token.AuthTokenViewSet


Module Contents
---------------

.. py:class:: AuthTokenSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.auth_token.AuthTokenSerializer
      :parts: 1


   .. py:attribute:: user


   .. py:attribute:: created_by


   .. py:attribute:: modified_by


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'user', 'token', 'name', 'description', 'text_format', 'is_active', 'start_date',...



      .. py:attribute:: read_only_fields
         :value: ['id', 'token', 'created_at', 'modified_at']



      .. py:attribute:: expandable_fields



.. py:class:: AuthTokenUpdateSerializer(instance=None, data=empty, **kwargs)

   Bases: :py:obj:`rest_framework.serializers.ModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.auth_token.AuthTokenUpdateSerializer
      :parts: 1


   Special serializer to prevent updating the user and token string.


   .. py:attribute:: user


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'user', 'name', 'description', 'text_format', 'is_active', 'start_date', 'end_date']




.. py:class:: AuthTokenFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`openbook.auth.filters.mixins.audit.CreatedModifiedByFilterMixin`, :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.auth_token.AuthTokenFilter
      :parts: 1


   .. py:attribute:: user


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



   .. py:method:: user_filter(queryset, name, value)


.. py:class:: AuthTokenViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.auth_token.AuthTokenViewSet
      :parts: 1


   Authentication tokens provide an authentication mechanism for remote clients without giving them
   a username and password. This allows human users to grant access (in their name) to other apps,
   though the apps then impersonate these human users. Thus, more importantly this allows to create
   special technical app users for which the access token is the only allowed authentication mechanism.


   .. py:attribute:: queryset


   .. py:attribute:: filterset_class


   .. py:attribute:: ordering
      :value: ['user__username', 'token']



   .. py:attribute:: search_fields
      :value: ['user__username', 'token', 'name', 'description']



   .. py:method:: get_serializer_class()

      Return the class to use for the serializer.
      Defaults to using `self.serializer_class`.

      You may want to override this if you need to provide different
      serializations depending on the incoming request.

      (Eg. admins get full serialization, others get basic serialization)



