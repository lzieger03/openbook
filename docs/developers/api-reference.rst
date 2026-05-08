=============
API Reference
=============

OpenBook exposes two HTTP APIs: a REST API for application data and an authentication API powered by
Django Allauth. Both are described by machine-readable OpenAPI schemas and come with an interactive
ReDoc browser you can use to explore endpoints and try requests during local development.

.. contents:: Page Content
   :local:


--------
REST API
--------

The OpenBook REST API contains machine-readable OpenAPI descriptions for clients to generate
typesafe remote stubs. Additionally, an interactive API browser using ReDoc is included.
The access the API, start the server with ``npm run start`` from the project root and open the
following URLs in a browser or API client:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Format
     - URL
   * - YAML schema
     - `http://localhost:8000/api/schema/ <http://localhost:8000/api/schema/>`_
   * - JSON schema
     - `http://localhost:8000/api/schema/?format=json <http://localhost:8000/api/schema/?format=json>`_
   * - Interactive ReDoc UI
     - `http://localhost:8000/api/schema/redoc/ <http://localhost:8000/api/schema/redoc/>`_


------------------
Authentication API
------------------

All things user management are handled by Django Allauth, which implements its own REST API.
The access the API, start the server with ``npm run start`` from the project root and open the
following URLs in a browser or API client:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Format
     - URL
   * - YAML schema
     - `http://localhost:8000/auth-api/openapi.yaml <http://localhost:8000/auth-api/openapi.yaml>`_
   * - JSON schema
     - `http://localhost:8000/auth-api/openapi.json <http://localhost:8000/auth-api/openapi.json>`_
   * - Interactive ReDoc UI
     - `http://localhost:8000/auth-api/openapi.html <http://localhost:8000/auth-api/openapi.html>`_
