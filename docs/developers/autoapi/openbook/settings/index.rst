openbook.settings
=================

.. py:module:: openbook.settings


Attributes
----------

.. autoapisummary::

   openbook.settings.BASE_DIR
   openbook.settings.SECRET_KEY
   openbook.settings.DEBUG
   openbook.settings.ALLOWED_HOSTS
   openbook.settings.OB_ROOT_REDIRECT
   openbook.settings.INSTALLED_APPS
   openbook.settings.MIDDLEWARE
   openbook.settings.ROOT_URLCONF
   openbook.settings.TEMPLATES
   openbook.settings.WSGI_APPLICATION
   openbook.settings.ASGI_APPLICATION
   openbook.settings.FORM_RENDERER
   openbook.settings.DATABASES
   openbook.settings.DEFAULT_AUTO_FIELD
   openbook.settings.CHANNEL_LAYERS
   openbook.settings.REST_FRAMEWORK
   openbook.settings.SPECTACULAR_SETTINGS
   openbook.settings.REST_FLEX_FIELDS2
   openbook.settings.AUTH_PASSWORD_VALIDATORS
   openbook.settings.AUTH_USER_MODEL
   openbook.settings.AUTHENTICATION_BACKENDS
   openbook.settings.ACCOUNT_ADAPTER
   openbook.settings.ACCOUNT_LOGIN_BY_CODE_ENABLED
   openbook.settings.ACCOUNT_LOGIN_BY_CODE_TIMEOUT
   openbook.settings.ACCOUNT_SIGNUP_FIELDS
   openbook.settings.ACCOUNT_EMAIL_VERIFICATION
   openbook.settings.ACCOUNT_USERNAME_BLACKLIST
   openbook.settings.ACCOUNT_USERNAME_MIN_LENGTH
   openbook.settings.SOCIALACCOUNT_ADAPTER
   openbook.settings.HEADLESS_ONLY
   openbook.settings.HEADLESS_ADAPTER
   openbook.settings.HEADLESS_SERVE_SPECIFICATION
   openbook.settings.HEADLESS_FRONTEND_URLS
   openbook.settings.USE_X_FORWARDED_HOST
   openbook.settings.SECURE_PROXY_SSL_HEADER
   openbook.settings.CSRF_COOKIE_SECURE
   openbook.settings.SESSION_COOKIE_SECURE
   openbook.settings.CRISPY_TEMPLATE_PACK
   openbook.settings.CRISPY_ALLOWED_TEMPLATE_PACKS
   openbook.settings.UNFOLD
   openbook.settings.INTERNAL_IPS
   openbook.settings.DEFAULT_FROM_EMAIL
   openbook.settings.EMAIL_SUBJECT_PREFIX
   openbook.settings.EMAIL_HOST
   openbook.settings.EMAIL_PORT
   openbook.settings.SITE_ID
   openbook.settings.LOGIN_REDIRECT_URL
   openbook.settings.USE_TZ
   openbook.settings.TIME_ZONE
   openbook.settings.LANGUAGE_CODE
   openbook.settings.USE_I18N
   openbook.settings.USE_L10N
   openbook.settings.USE_THOUSAND_SEPARATOR
   openbook.settings.STATIC_URL
   openbook.settings.STATIC_ROOT
   openbook.settings.STATICFILES_DIRS
   openbook.settings.MEDIA_URL
   openbook.settings.MEDIA_ROOT
   openbook.settings.DBBACKUP_STORAGE
   openbook.settings.DBBACKUP_STORAGE_OPTIONS
   openbook.settings.EXTRA_INSTALLED_APPS


Module Contents
---------------

.. py:data:: BASE_DIR

.. py:data:: SECRET_KEY
   :value: 'django-insecure-jeo+.}_}9(Q.t_IU$WJ!%eL=b:MDbAL.~NY_=a:>D@:W[XPh4['


.. py:data:: DEBUG
   :value: True


.. py:data:: ALLOWED_HOSTS
   :value: ['*']


.. py:data:: OB_ROOT_REDIRECT
   :value: '/app/index.html'


.. py:data:: INSTALLED_APPS
   :value: ['openbook.core', 'openbook.auth', 'openbook.content', 'daphne', 'channels', 'rest_framework',...


.. py:data:: MIDDLEWARE
   :value: ['django.middleware.security.SecurityMiddleware',...


.. py:data:: ROOT_URLCONF
   :value: 'openbook.urls'


.. py:data:: TEMPLATES

.. py:data:: WSGI_APPLICATION
   :value: 'openbook.wsgi.application'


.. py:data:: ASGI_APPLICATION
   :value: 'openbook.asgi.application'


.. py:data:: FORM_RENDERER
   :value: 'django.forms.renderers.DjangoTemplates'


.. py:data:: DATABASES

.. py:data:: DEFAULT_AUTO_FIELD
   :value: 'django.db.models.BigAutoField'


.. py:data:: CHANNEL_LAYERS

.. py:data:: REST_FRAMEWORK

.. py:data:: SPECTACULAR_SETTINGS

.. py:data:: REST_FLEX_FIELDS2

.. py:data:: AUTH_PASSWORD_VALIDATORS

.. py:data:: AUTH_USER_MODEL
   :value: 'openbook_auth.User'


.. py:data:: AUTHENTICATION_BACKENDS
   :value: ('openbook.auth.backends.RoleBasedObjectPermissionsBackend',...


.. py:data:: ACCOUNT_ADAPTER
   :value: 'openbook.auth.allauth.adapter.AccountAdapter'


.. py:data:: ACCOUNT_LOGIN_BY_CODE_ENABLED
   :value: True


.. py:data:: ACCOUNT_LOGIN_BY_CODE_TIMEOUT
   :value: 300


.. py:data:: ACCOUNT_SIGNUP_FIELDS
   :value: ['username*', 'email*', 'password1*', 'password2*']


.. py:data:: ACCOUNT_EMAIL_VERIFICATION
   :value: 'mandatory'


.. py:data:: ACCOUNT_USERNAME_BLACKLIST
   :value: ['admin', 'Administrator', 'root', 'superuser']


.. py:data:: ACCOUNT_USERNAME_MIN_LENGTH
   :value: 5


.. py:data:: SOCIALACCOUNT_ADAPTER
   :value: 'openbook.auth.allauth.adapter.SocialAccountAdapter'


.. py:data:: HEADLESS_ONLY
   :value: False


.. py:data:: HEADLESS_ADAPTER
   :value: 'allauth.headless.adapter.DefaultHeadlessAdapter'


.. py:data:: HEADLESS_SERVE_SPECIFICATION
   :value: True


.. py:data:: HEADLESS_FRONTEND_URLS

.. py:data:: USE_X_FORWARDED_HOST
   :value: True


.. py:data:: SECURE_PROXY_SSL_HEADER
   :value: ('HTTP_X_FORWARDED_PROTO', 'https')


.. py:data:: CSRF_COOKIE_SECURE
   :value: True


.. py:data:: SESSION_COOKIE_SECURE
   :value: True


.. py:data:: CRISPY_TEMPLATE_PACK
   :value: 'unfold_crispy'


.. py:data:: CRISPY_ALLOWED_TEMPLATE_PACKS
   :value: ['unfold_crispy']


.. py:data:: UNFOLD

.. py:data:: INTERNAL_IPS
   :value: ['127.0.0.1']


.. py:data:: DEFAULT_FROM_EMAIL
   :value: 'noreply@example.com'


.. py:data:: EMAIL_SUBJECT_PREFIX
   :value: '[OpenBook] '


.. py:data:: EMAIL_HOST
   :value: 'localhost'


.. py:data:: EMAIL_PORT
   :value: 1025


.. py:data:: SITE_ID
   :value: 1


.. py:data:: LOGIN_REDIRECT_URL
   :value: '/'


.. py:data:: USE_TZ
   :value: True


.. py:data:: TIME_ZONE
   :value: 'UTC'


.. py:data:: LANGUAGE_CODE
   :value: 'en-us'


.. py:data:: USE_I18N
   :value: True


.. py:data:: USE_L10N
   :value: True


.. py:data:: USE_THOUSAND_SEPARATOR
   :value: True


.. py:data:: STATIC_URL
   :value: 'static/'


.. py:data:: STATIC_ROOT

.. py:data:: STATICFILES_DIRS

.. py:data:: MEDIA_URL
   :value: 'media/'


.. py:data:: MEDIA_ROOT

.. py:data:: DBBACKUP_STORAGE
   :value: 'django.core.files.storage.FileSystemStorage'


.. py:data:: DBBACKUP_STORAGE_OPTIONS

.. py:data:: EXTRA_INSTALLED_APPS
   :value: []


