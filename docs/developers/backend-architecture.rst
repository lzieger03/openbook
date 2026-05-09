====================
Backend Architecture
====================

This page collects defining aspects of the OpenBook backend architecture. The intention is to help
developers understand the most important technology and implementation choices.

.. contents:: Page Content
   :local:


------------------
Technology Choices
------------------

The OpenBook Server is built with the following technology:

.. list-table::
   :width: 100%
   :widths: 1 2

   * - **Python**
     - Programming language
   * - **Poetry**
     - Package manager
   * - **Django Web Framework**
     - Core server framework
   * - **Django Allauth**
     - Authentication, user management, single sign-on
   * - **Django REST Framework**
     - RESTS API for the frontend and external clients
   * - **Django Channels**
     - WebSocket support
   * - **Celery**
     - Background tasks

The idea is to keep the technical requirements lean to enable easy deployment in custom environments.
Therefore, the choice of Django might be considered "conservative", but in fact it contains all
needed functionality, like HTTP request routing, server-side templates, and database access, in a
single, stable, and well-maintained dependency.


-------------------
Permission Handling
-------------------

This section describes permission handling in Django and how it is used in the application. It
explains the implementation strategy to make regular model-based permissions (for example,
"Can create textbook") co-exist with object-level permissions (for example,
"Can change THIS textbook").

Default Permissions for Each Model
..................................

When the app ``django.contrib.auth`` is installed, Django automatically creates four permission objects
in the database for each model:

.. list-table::
   :header-rows: 1
   :width: 100%
   :widths: 1 2

   * - Permission
     - Meaning
   * - ``{app_label}.add_{model}``
     - Add new objects
   * - ``{app_label}.view_{model}``
     - Search and display objects
   * - ``{app_label}.change_{model}``
     - Modify existing objects
   * - ``{app_label}.delete_{model}``
     - Delete existing objects

``{app_label}`` is the owning app's label (as defined in the ``App`` class), and ``{model}`` is the name
of the model in lower-case (no other transformation done).

How Permissions Are Checked (on Model Level)
............................................

**Django Admin** -- By default, model permissions are checked in the Django Admin (in the
``ModelAdmin`` class, methods ``has_..._permission(self, request)``) to check whether a user is allowed
to perform the corresponding action.

**Own Code** -- No permissions check is done when directly accessing the database with the Django ORM.
Permission checks must be performed in the higher levels (views), of which the Django Admin happens
to be one. The easiest way to check a permission is to call ``has_perm()`` on the user object, for
example ``user.has_perm("myapp.view_model")``. This in turn iterates over the installed authentication
backends and calls ``has_perm(user_obj, perm)`` until one backend grants the permission.

**Django REST Framework** -- Django REST Framework does not do permission checks unless specifically
asked in the ``ViewSet``. Permission checks are encapsulated in ``permission_classes`` that may
implement arbitrary logic. These classes inherit from a ``BasePermission`` that defines the method
``has_permission(self, request, view)``. Most implementations do not use the ``django.contrib.auth``
permissions but rather implement simpler checks like ``IsAuthenticated`` or ``AllowAny``.
``DjangoModelPermissions`` applies permission checks similar to Django Admin's ``ModelAdmin``, though
they do not share any code.

When a ``ViewSet`` contains multiple permission classes as a list, permission is only granted if all
of them return ``True``:

.. code-block:: python

   class MyModelViewSet(ModelViewSet):
      queryset = MyModel.objects.all()
      serializer_class = MyModelSerializer
      permission_classes = [IsAuthenticated, IsStaff, IsOwner]

However, permissions can also be combined using logic operators, for example:

.. code-block:: python

   class MyModelViewSet(ModelViewSet):
      # ...
      permission_classes = IsAuthenticated & (IsStaff | IsOwner)

How Object-Level Permissions Are Checked
........................................

Object-level permissions always require a custom authentication backend, as Django only includes the
API. The API is a compatible extension to the regular API:

.. list-table::
   :header-rows: 1
   :width: 100%

   * - Extension Point
     - API
   * - Django User
     - ``User.has_perm(self, perm, obj=None)``
   * - Authentication Backend
     - ``has_perm(user_obj, perm, obj=None)``
   * - Django Admin
     - ``ModelAdmin.has_..._permission(self, request, obj=None)``
   * - Django REST Framework
     - ``BasePermission.has_object_permission(self, request, view, obj)``

However, there are some oddities:

**Query Set Visibility** --- Neither Django, Django Admin, nor Django REST Framework apply object
permissions to query sets. This means users can always query objects and read all data even when
they lack "view" permissions.

**Default ModelBackend Behavior** --- Django's default ``ModelBackend`` always returns ``False`` when
object-level permissions are checked, even when the user has the global permission.

**ModelAdmin Object Parameter** --- ``ModelAdmin`` ignores the ``obj`` parameter and always checks
model permissions.

**Create Permission Gap in DRF** --- Django REST Framework checks object-level permissions only in
class ``DjangoObjectPermissions``, but despite the documentation it seems the add permission is not
checked (because the new object does not yet exist).

**Limitations Around get_object()** --- Django REST Framework checks object permissions in the
``get_object()`` method. It may be necessary to manually call the inherited method when it is
replaced with a custom implementation or when the generic REST views are not used. Limitations of
object permissions in Django REST Framework
(`Source <https://www.django-rest-framework.org/api-guide/permissions/>`_):

.. rst-class:: spaced-list

* For performance reasons, the generic views will not automatically apply object-level permissions
  to each instance in a queryset when returning a list of objects.

* Often, when using object-level permissions, you will also want to filter the queryset
  appropriately to ensure that users only have visibility onto instances that they are permitted to
  view.

* Because the ``get_object()`` method is not called, object-level permissions from the
  ``has_object_permission()`` method are not applied when creating objects. In order to restrict
  object creation, you need to implement the permission check either in your ``Serializer`` class or
  override the ``perform_create()`` method of your ``ViewSet`` class.

How Our Custom Authentication Backend Is Implemented
....................................................

**Adding Roles to Models** -- Our permission system is built around the premise that some models
support object permissions and others do not. Models supporting object permissions implement the
``ScopedRolesMixin`` to become a scope for user roles and related objects:

.. list-table::
   :header-rows: 1
   :width: 100%

   * - Concept
     - Meaning
   * - Roles
     - Exist within the scope and collect Django ``Permission`` entries.
   * - Allowed Permissions
     - Define which permissions can be added to the roles of a scope.
   * - Role Assignments
     - Assign roles to users within the scope.
   * - Access Requests
     - Can be created by users to request a role within a scope.
   * - Enrollment Methods
     - Allow users to self-enroll to get a role within a scope.
   * - Public Permissions
     - Are permissions for non-enrolled and anonymous users within a scope.

Typical scopes are courses and textbooks. They often contain related objects (for example, course
materials or textbook pages) that also support object permissions but share the scope of their parent
object. This allows permissions like "In this course (scope object), teachers (role) can create
materials (related object)" to be expressed. For this, the related objects must inherit
``RoleBasedObjectPermissionsMixin`` and override the ``get_scope()`` method. In both cases (scope
objects and related objects), the method ``has_perm()`` can be overridden to implement additional
custom checks.

**Authentication Backend** -- We provide a custom authentication backend in class
``openbook.core.RoleBasedObjectPermissionsBackend``, as it appears simpler than reusing third-party
libraries. Especially libraries like Django Guardian require explicitly persisting and keeping in
sync who can do what for which single object.

``RoleBasedObjectPermissionsBackend`` inherits from the stock ``ModelBackend`` and changes its behavior
as follows: For normal permission checks without an object, it behaves exactly the same. Object
permissions are checked in the following order, stopping at the first match:

1. The user is a superuser.
2. The user and the object are the same.
3. The user is the object's ``owner`` (optional).
4. The object's ``has_obj_perm()`` method (via mixins, optional).

   1. Public permissions of the scope.
   2. Roles assigned to the user.

5. Regular non-object permissions.

Superusers can do anything. Users can change their own data. The owner is always authorized.
Otherwise, role-based permissions are checked. If this is not supported by the object or fails, it
falls back to regular user permissions. Thus, the ``ModelBackend`` does not need to be included in the
Django settings, as its function is already covered.

The Django Admin first checks "view" then "change" permissions when a single object should be
displayed. This logic has been moved to our ``RoleBasedObjectPermissionsBackend`` to unify the behavior
in all parts of the application.

How We Iron Out the Inconsistencies
...................................

**Querying and Filtering** -- No deliberate attempt is done on the technical level to restrict query
results to objects where the user has view permissions. Applying several database joins would in
theory be possible, but it seems not worth the effort or performance loss. Instead, we should be
cautious to return as few fields as possible when models are searched and queried, always assuming
that the returned values could be visible to anyone.

**Django Admin** -- Use ``openbook.core.admin.utils.model.ModelAdmin`` instead of the stock
``ModelAdmin`` to make sure that object-level permissions are checked for displaying, changing, and
deleting single objects. Unlike the stock class, this version applies a hack to check object
permissions also for new objects ("add").

**Django REST Framework** -- We set our own ``AllowNone`` default permission in ``settings.py`` to
enforce a deliberate decision for each view set and prevent unprotected REST endpoints by accident.

The module ``openbook.core.drf`` contains specialized ``ModelSerializer`` and ``ModelViewSet`` classes
that use ``DjangoObjectPermissionsOnly`` by default, run a ``full_clean()`` on the object before it is
saved (to run validations implemented in the model layer), and check object permissions also when new
objects are created (POST). These two classes also employ a hack to check object permissions for new
objects ("add").

``DjangoObjectPermissionsOnly`` is a specialized version of the stock ``DjangoObjectPermissions`` that
respects the logic in our authentication backend (model permission is not required but overrides
object permission, and view permission is checked too).
