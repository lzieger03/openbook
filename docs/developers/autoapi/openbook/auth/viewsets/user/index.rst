openbook.auth.viewsets.user
===========================

.. py:module:: openbook.auth.viewsets.user


Classes
-------

.. autoapisummary::

   openbook.auth.viewsets.user.UserSerializer
   openbook.auth.viewsets.user.CurrentUserSerializer
   openbook.auth.viewsets.user.UserFilter
   openbook.auth.viewsets.user.UserViewSet
   openbook.auth.viewsets.user.CurrentUserViewSet


Module Contents
---------------

.. py:class:: UserSerializer

   Bases: :py:obj:`openbook.drf.flex_serializers.FlexFieldsModelSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.user.UserSerializer
      :parts: 1


   .. py:attribute:: full_name


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'username', 'full_name', 'first_name', 'last_name', 'description', 'picture', 'is_staff',...



      .. py:attribute:: read_only_fields
         :value: ['username', 'is_staff']



      .. py:attribute:: filterset_fields
         :value: ['first_name', 'last_name', 'is_staff']



      .. py:attribute:: expandable_fields



   .. py:method:: get_full_name(obj)


.. py:class:: CurrentUserSerializer

   Bases: :py:obj:`UserSerializer`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.user.CurrentUserSerializer
      :parts: 1


   .. py:attribute:: is_authenticated


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields
         :value: ['id', 'username', 'full_name', 'first_name', 'last_name', 'description', 'picture', 'is_staff',...



      .. py:attribute:: filterset_fields
         :value: ['first_name', 'last_name', 'is_staff']




.. py:class:: UserFilter(data=None, queryset=None, *, request=None, prefix=None)

   Bases: :py:obj:`django_filters.filterset.FilterSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.user.UserFilter
      :parts: 1


   .. py:class:: Meta

      .. py:attribute:: model


      .. py:attribute:: fields



.. py:class:: UserViewSet(**kwargs)

   Bases: :py:obj:`openbook.drf.viewsets.ModelViewSetMixin`, :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.user.UserViewSet
      :parts: 1


   Read/write view set to query active users and update/delete the own user profile.


   .. py:attribute:: lookup_field
      :value: 'username'



   .. py:attribute:: queryset


   .. py:attribute:: http_method_names
      :value: ['get', 'put', 'patch', 'delete']



   .. py:attribute:: filterset_class


   .. py:attribute:: serializer_class


   .. py:attribute:: ordering
      :value: ['username']



   .. py:attribute:: search_fields
      :value: ['username', 'first_name', 'last_name', 'description']



.. py:class:: CurrentUserViewSet(**kwargs)

   Bases: :py:obj:`rest_framework.viewsets.ModelViewSet`

   .. autoapi-inheritance-diagram:: openbook.auth.viewsets.user.CurrentUserViewSet
      :parts: 1


   GET endpoint to retrieve the user profile of the currently logged-in user. If the
   user is not logged in, a simple response with `is_authenticated = false` is returned.


   .. py:attribute:: permission_classes


   .. py:attribute:: serializer_class


   .. py:attribute:: queryset


   .. py:method:: get_view_name()

      Return the view name, as used in OPTIONS responses and in the
      browsable API.



   .. py:method:: list(request)


   .. py:method:: retrieve(request, pk=None)
      :abstractmethod:



