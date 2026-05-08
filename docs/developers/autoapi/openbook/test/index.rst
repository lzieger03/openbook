openbook.test
=============

.. py:module:: openbook.test


Attributes
----------

.. autoapisummary::

   openbook.test.User


Classes
-------

.. autoapisummary::

   openbook.test.ModelViewSetTestMixin


Module Contents
---------------

.. py:data:: User

.. py:class:: ModelViewSetTestMixin

   Shared unit tests for the ModelViewSet based REST APIs. Defines parametrized unit tests for
   common behavior like searching, sorting and the usual REST HTTP methods. Use it like this:

   ```python
   class MyModel_ViewSet_Test(ModelViewSetTestMixin, TestCase):
       base_name         = "my_model"
       model             = MyModel
       pk_found          = 4711,
       search_string     = "test"
       search_count      = 2
       sort_field        = "fieldname"
       expandable_fields = ("fk_relation", "m2m_relation[]")

       def get_create_data(self):
           return {...}

       operations = {
           "create": {
               "request_data": get_create_data,    # Dict or method that returns dict
           },
           "update": {
               "request_data": {"some_field": "new value"},
               "updates": {"some_obj": {"id": "new_value"}},
           },
           "partial_update": {
               "request_data": {...},
               "updates": {...},
           },

           # Not supported operation
           "delete": {
               "supported": False,
           },

           # Custom action (without authentication/authorization)
           "custom": {
               "supported":          True,
               "http_method":        ModelViewSetTestMixin.HttpMethod.GET,
               "status_code":        200,      # Okay
               "url_suffix":         "custom",
               "requires_auth":      False,
               "model_permission":   (),
               "assertions":         (assertHealthStatus,),
           },
       }
   ```

   See the source of this class for all supported properties. There are lots more to cover
   special cases like custom permissions, non-authenticated operations and so on.

   Use a custom assertion method to check the object after updates, if the check based on the
   `"updates"` dict is too simple.

   This mixin creates lots of additional test methods via meta-programming to assert that
   for each endpoint (operation) the REST API uses authentication, authorization, returns
   the expected status code and performs the expected actions. Additional test methods may
   be manually created as usual, to test special behavior beyond this.


   .. py:class:: HttpMethod

      .. py:attribute:: GET


      .. py:attribute:: PUT


      .. py:attribute:: POST


      .. py:attribute:: PATCH


      .. py:attribute:: DELETE



   .. py:attribute:: base_name
      :value: 'change_me'


      Base name as defined in the DRF router


   .. py:attribute:: model
      :type:  django.db.models.Model
      :value: None


      Model class for automatically determining required permissions


   .. py:attribute:: count
      :type:  int
      :value: 0


      Expected list count, if not just all model entries. Set to < 0 to disable, or > 0 to override database lookup.


   .. py:attribute:: pk_field
      :value: 'pk'


      Name of the key field of the model (for testing that DELETE actually deletes the object)


   .. py:attribute:: pk_found
      :value: 'change-me'


      String or method to get key value of an existing object for testing the detail operations


   .. py:attribute:: pk_not_found
      :value: 'not-found'


      String or method to get key value of a non-existing object for testing the 404 status code


   .. py:attribute:: search_string
      :value: ('',)


      Search string to test the `_search` query parameter (will not be tested if string is empty)


   .. py:attribute:: search_count
      :value: -1


      Number of expected search results when testing the `_search` query parameter


   .. py:attribute:: sort_field
      :value: ''


      Fieldname to test the `_sort` query parameter (will not be tested if string is empty)


   .. py:attribute:: expandable_fields
      :value: ()


      List of expandable relation fields to test that expansion doesn't crash. Fields ending with `[]` are tested as lists.


   .. py:attribute:: operations

      Test configuration for each supported operation. Contains all the standard operations like
      "list", "change", etc. but you can also add additional entries for custom actions defined
      with the `@action` decorator in the view set. In that case use the constants defined in the
      inner class `HttpMethod` to set the HTTP method for the new operation. The expected status
      codes will be automatically determined as per the other values.

      When adding custom actions, make sure to set the `"url_suffix"` to the action name and to
      set `"url_has_pk"` to `True`, when it is an action for a single object.

      For unsupported operations the key `"supported"` should be set to `False`. This lets the test
      case test that it is really unsupported.

      Note, that test users will be automatically created to test the permissions. The permissions
      will be directly assigned to the users as user permissions. Scoped permissions need to be
      checked separately, but usually it is not necessary to test scoped permissions for each view
      set. It is sufficient to test that scoped permissions work in general.


   .. py:method:: setUp()


   .. py:method:: login(username = None, password = None)

      (Re)login with another user.



   .. py:method:: create_user_and_login(perm_strings)

      Create new user with the given permissions and login.



   .. py:method:: logout()

      Logout.



   .. py:method:: assertStatusCode(response, expected_status_code)

      Assert status code in HTTP response.



   .. py:method:: assertResultList(response, expected_count)

      Assert response data contains a result list with the expected number of entries.
      The result count will only be checked if `expected_count` is at least zero.



   .. py:method:: assertSortOrder(response, sort_field)

      Assert that the result list is sorted as expected.



   .. py:method:: assertFieldsExpanded(response, expandable_fields)

      Assert that the given fields have been expanded to objects or lists with objects.



   .. py:method:: assertObjectCreated(response, pk_field, pk_found)

      Assert that the object with the given key has been created.



   .. py:method:: assertObjectDeleted(response, pk_field, pk_found)

      Assert that the object with the given key has been deleted.



   .. py:method:: assertObjectUpdated(response, pk_field, pk_found, updates)

      Assert that updates were fully applied.



