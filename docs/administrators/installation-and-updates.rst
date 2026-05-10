========================
Installation and Updates
========================

This page summarizes how to deploy OpenBook in production, which components are involved, and
which operational tasks administrators should plan for. It is a direct RST adaptation of the
legacy deployment notes for Linux operators who manage reverse proxies, databases, and Django
services.

.. contents:: Page Content
   :local:


-----------
Quick Start
-----------

System Overview
...............

OpenBook is a standard Django deployment with a few project-specific considerations. The general
deployment process follows the `Django documentation <https://docs.djangoproject.com/en/5.0/#the-development-process>`_.
This page focuses on the concrete parts that matter when you run OpenBook in production.

.. figure:: img/deployment-architecture.png
   :align: center
   :alt: Deployment architecture with reverse proxy, ASGI app, SQL database, and optional Redis.

   OpenBook deployment architecture and component boundaries.

The deployment can stay simple at first. A single machine can host the reverse proxy, the ASGI
application, the database, and optional supporting services. If the reverse proxy can distribute
traffic across several backend processes, the same layout also scales to multiple application
instances later.

**Front Web Server** -- A front web server is not strictly required, but it is the usual choice for
TLS termination, static file delivery, uploaded media delivery, and reverse proxying to the Django
application. In a small installation, one machine often serves all of these roles. In a larger
installation, static files, media files, and the application can be separated across domains or
machines. Apache HTTP Server remains a common production choice, while `Caddy <https://caddyserver.com/>`_
is a good modern alternative with minimal configuration.

.. code-block:: apache

   # this can go in either server config, virtual host, directory or .htaccess
   WSGIPassAuthorization On

**ASGI Server** -- The core application runs through an ASGI server. For Django projects this is
commonly `Daphne <https://github.com/django/daphne>`_, which is already part of the project
dependencies. A typical production command is:

.. code-block:: bash

   daphne -p 8000 -b 0.0.0.0 openbook.asgi:application

**Redis** -- OpenBook incroporates real-time features based on Django Channels and Celery. These
require a running Redis service to decouple the main web process from background and task runners.
While these can run on many different queues, Redis is the usual backend. The pre-defined Django
configuration expects Redis on ``localhost:6379`` by default, although you can override that in
the local settings.

**Database** -- OpenBook needs a SQL database for persistent storage. `MariaDB
<https://mariadb.org/>`_ and `PostgreSQL <https://www.postgresql.org/>`_ are both suitable
choices. Refer to the `Django database documentation
<https://docs.djangoproject.com/en/5.0/ref/databases/>`_ for supported backends, install the
matching Python driver, and update the deployment settings accordingly.

Docker Compose
..............

The :file:`docker/` directory contains a working Docker Compose example that you can use as a reference
deployment and as a starting point for your own environment. It is useful both for local deployment
tests and for understanding how the components fit together.

The most common Docker Compose commands are:

* :command:`docker compose build` to build the images
* :command:`docker compose up` to start the stack in the foreground
* :command:`docker compose up -d` to start the stack in the background
* :command:`docker compose down` to stop the stack
* :command:`docker exec -it docker-openbook-server-1 sh` to open a shell in the application container

The example setup defines the following services:

* ``postgres`` in container ``docker-postgres-1`` for persistent database storage
* ``redis`` in container ``docker-redis-1`` for asynchronous processing support
* ``openbook-server`` in container ``docker-openbook-server-1`` for the Django application
* ``webserver`` in container ``docker-webserver-1`` for the front-facing reverse proxy

There is currently no official image on Docker Hub. The repository instead provides a Dockerfile
that Compose builds locally. The legacy deployment recommendation still applies: copy the
:file:`docker/` directory to a location outside the Git checkout and adapt it to your environment.

-------------------
Manual Installation
-------------------

TODO: Step-by-step installation tutorial showing how to download and install OpenBook.
Using a minimal Debian server as an example. Steps can be easily transfered to other environments.
For the sake of simplicity:
   - Everything running on the same host.
   - Source code downloaded from the GitHub release page (or cloning a version branch via Git)
   - New Python environment under /opt/openbook (managed with Poetry)
   - System services like DB or Redis installed via OS package manager.
   - Regular background jobs via Cron
   - Automatic start-up of required services and processes via SystemD.
Two web server options covered:
   - Traditionall: Apache + certbot (the latter for Let's Encrypt TLS certificats)
   - Slim: Caddy (already handles Let's Encrypt by defualt)

---------------
Troubleshooting
---------------

OS Dependencies (xmlsec1, ltdl)
...............................

Before you install Python dependencies with :command:`poetry install`, make sure the required system
packages for SAML support are present. On Linux, install them through your distribution package
manager.

* ``xmlsec1`` including development headers
* ``libtool-ltdl`` including development headers

These packages are required for SAML integration. If you do not plan to use SAML and cannot install
them, you can edit :file:`pyproject.toml` and remove ``"saml"`` from the ``django-allauth`` dependency
extras.

If the server later crashes with ``xmlsec.InternalError: (-1, 'lxml & xmlsec libxml2 library
version mismatch')``, the cause is usually one of the following:

* The system has multiple ``libxml2`` versions installed.
* ``lxml`` and ``xmlsec`` were compiled against different ``libxml2`` versions.
* ``libxml2``, ``lxml``, or ``xmlsec`` changed without rebuilding the others.
* Poetry installed binary wheels that do not match the system libraries.

In many cases, reinstalling both packages from source resolves the mismatch::
In many cases, reinstalling both packages from source resolves the mismatch:

.. code-block:: bash

   poetry run pip uninstall lxml xmlsec -y
   poetry run pip install --no-binary=:all: lxml xmlsec


Local Django Settings
.....................

Deployment-specific configuration is separated from the shared Django settings through a local
override file. This keeps must-have settings, required to run OpenBook at all, in version control
while defining a clear place for database connections, credentials and other site-specific settings.

.. list-table:: Periodic Management Commands
   :header-rows: 1
   :width: 100%

   * - File
     - User Changeable
     - Content
   * - :file:`settings.py`
     - No
     - Core Django settings
   * - :file:`local_settings.py`
     - Yes
     - Installation-specific settings, e.g. database connections

The :file:`local_settings.py` file is therefore excluded from version control. A template file in the
repository documents the settings that administrators commonly need to adjust.

WSGI vs. ASGI
.............

Traditional WSGI deployments with Apache and mod_python are not sufficient here because OpenBook
also relies on Django Channels and therefore expects an ASGI-capable application server. Daphne is
already included, so the basic startup command is straightforward.

To start the application and listen on all interfaces::
To start the application and listen on all interfaces:

.. code-block:: bash

   cd src
   daphne -p 8000 -b 0.0.0.0 openbook.asgi:application

On a local workstation you may need to run Daphne through Poetry so it uses the project virtual
environment.

If the application sits behind a reverse proxy on the same host, bind it to localhost instead:

.. code-block:: bash

   cd src
   daphne -p 8000 openbook.asgi:application

If you still need a reverse proxy, `Caddy <https://caddyserver.com/>`_ is a practical option.

Do not forget static and uploaded media files. By default, OpenBook stores them in :file:`_static/` and
:file:`_media/` within the Django project, although the file system paths and public URLs can be
overridden in :file:`local_settings.py`. After changing static asset settings, collect the files before
serving them:

.. code-block:: bash

   python ./manage.py collectstatic

Authorization Headers
.....................

When the web server proxies API requests, make sure it forwards authorization headers. The `Django
REST framework authentication guide <https://www.django-rest-framework.org/api-guide/authentication/#apache-mod_wsgi-specific-configuration>`_
notes that Apache with mod_wsgi does not pass the ``Authorization`` header by default. In that
case, enable it explicitly:

Periodic Jobs
.............

OpenBook includes Django management commands that should run periodically to keep the deployment
clean and predictable. In practice you would call them through cron, a systemd timer, or another
job scheduler.

The commands are typically run from the Django project directory::
The commands are typically run from the Django project directory:

.. code-block:: bash

   ./manage.py command --options

The most important periodic tasks are listed below.

.. list-table:: Periodic Management Commands
   :header-rows: 1
   :width: 100%

   * - Management Command
     - Description
   * - :command:`clearsessions`
     - Removes expired sessions from the database.
   * - :command:`remove_stale_contenttypes --no-input`
     - Removes stale content types for non-existing models.

Backup Commands
...............

OpenBook includes `Django DBBackups <https://django-dbbackup.readthedocs.io/>`_ for database and
media backups. Backups can be written to local storage or to remote destinations such as S3 or
Dropbox. The upstream project documentation covers the full configuration model. The table below
summarizes the commands that administrators use most often.

.. list-table:: Backup Management Commands
   :header-rows: 1
   :width: 100%

   * - Management Command
     - Description
   * - :command:`dbbackup`
     - Creates a new database backup.
   * - :command:`dbrestore`
     - Restores a database backup into an empty database.
   * - :command:`listbackups`
     - Lists the available backups.
   * - :command:`mediabackup`
     - Creates a backup of uploaded media files.
   * - :command:`mediarestore`
     - Restores uploaded media files from backup storage.

The target database should be empty before you restore a backup. For larger installations, the
DBBackups documentation recommends creating backups from a database replica to reduce load on the
primary database server.

SAML SSO and Social Login
.........................

OpenBook uses `django-allauth[saml]
<https://docs.allauth.org/en/latest/socialaccount/providers/saml.html>`_ for SAML identity
providers. The same authentication stack can also support local user registration and common social
login providers such as Google or Microsoft. A few project-specific hints are documented in
:file:`local_settings.py`, but the `django-allauth documentation
<https://docs.allauth.org/en/latest/index.html>`_ remains the authoritative reference.

If you load the initial test data, the system already contains a dummy SAML provider based on
`mocksaml.com <https://mocksaml.com>`_ from Ory. For a full signup and login test, also check the
local mail capture service at `http://localhost:8887 <http://localhost:8887>`_ so you can complete account verification.
The test setup recognizes two mail domains and maps them to different user groups:

* ``example.com`` creates users in the ``student`` group.
* ``example.org`` creates users in the ``teacher`` group.

The allauth SAML guidelines highlight a few operational requirements that are easy to miss:

Most SAML identity providers require HTTPS, so plain :command:`runserver`-style testing is usually not
enough for realistic validation. Mock SAML is a practical exception and can work over HTTP, but
production-like tests should still run with TLS enabled.

When OpenBook is deployed behind a reverse proxy, configure Django to trust forwarded protocol and
host information by enabling ``USE_X_FORWARDED_HOST = True``,
``SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')``, and
``SECURE_SSL_REDIRECT = True``. The reverse proxy must also forward protocol metadata correctly so
that Django can reliably detect HTTPS requests.

Cookie settings should match the real deployment domain. Set ``CSRF_COOKIE_DOMAIN`` and
``SESSION_COOKIE_DOMAIN`` accordingly, and enable ``CSRF_COOKIE_SECURE`` and
``SESSION_COOKIE_SECURE`` to ensure cookies are only transmitted over HTTPS. During SAML testing,
run login flows in browser privacy mode, inspect the network exchange in developer tools, and use a
tracer such as SAML Tracer to verify the exchanged assertions and attribute mappings.
