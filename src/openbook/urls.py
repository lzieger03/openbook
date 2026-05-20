# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf                     import settings
from django.conf.urls.static         import static
from django.views.generic.base       import RedirectView
from django.views.static             import serve
from django.urls                     import include
from django.urls                     import path
from django.urls                     import re_path
from drf_spectacular.views           import SpectacularAPIView
from drf_spectacular.views           import SpectacularRedocView
from rest_framework.permissions      import IsAuthenticatedOrReadOnly
from rest_framework.routers          import DefaultRouter as DRFDefaultRouter

from .admin                          import admin_site
from .auth.routes                    import register_api_routes as register_auth_api_routes
from .core.routes                    import register_api_routes as register_core_api_routes
from .content.routes                 import register_api_routes as register_course_api_routes
from .gamification.routes            import register_api_routes as register_gamification_api_routes


def serve_spa_index(request, path=""):
    """Serve index.html for all routes under /app/ to support SPA routing."""
    spa_dir = f"{settings.BASE_DIR}/frontend/app/dist/openbook/app"
    
    # Check if the request is for a file (has a file extension)
    if "." in path.split("/")[-1]:
        return serve(request, path, document_root=spa_dir)
    
    # Otherwise, serve index.html for SPA routing
    return serve(request, "index.html", document_root=spa_dir)

# Overwrite permission class for API root view, since it uses the default from settings.py,
# which would only allow authenticated users to see the API documentation.
DRFDefaultRouter.APIRootView.permission_classes = [IsAuthenticatedOrReadOnly]
api_router = DRFDefaultRouter()

register_auth_api_routes(api_router, "auth")
register_core_api_routes(api_router, "core")
register_course_api_routes(api_router, "content")
register_gamification_api_routes(api_router, "gamification")

urlpatterns = [
    # REST API
    path("api/",              include(api_router.urls)),
    path("api/schema/",       SpectacularAPIView.as_view(), name="api-schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="api-schema"), name="api-redoc"),

    # Admin Panel
    path("admin/",            admin_site.urls),

    # User Accounts
    path("accounts/",         include("allauth.urls")),
    path("auth-api/",         include("allauth.headless.urls")),

    # Single Page App - Handle all app routes with index.html
    re_path(r"^app(?:/(?P<path>.*))?$", serve_spa_index, name="spa"),

    # Root redirect
    path("",                  RedirectView.as_view(url=settings.OB_ROOT_REDIRECT)),
]

if settings.DEBUG:
    # NOTE: Static files are automatically served by runserver from the configured
    # static dirs (usually inside each application)

    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
