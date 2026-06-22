# OpenBook: Interactive Online Textbooks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from __future__ import annotations

from django.conf                           import settings
from django.contrib.auth.models            import AbstractUser
from django.contrib.auth.decorators        import login_required
from django.contrib.auth.views             import redirect_to_login
from django.http                           import HttpRequest
from django.http                           import HttpResponse
from django.shortcuts                      import redirect
from django.views.static                   import serve

# Name of the Django group whose members are treated as teachers.
TEACHER_GROUP_NAME = "Teacher"

# Frontends users are sent to after login depending on their role.
TEACHER_REDIRECT_URL = "/teacher/"
STUDENT_REDIRECT_URL = "/dashboard/index.html"

def is_teacher(user: AbstractUser | None) -> bool:
    """
    Return whether the user counts as a teacher (member of the ``Teacher`` group).
    """
    return (
        user is not None
        and user.is_authenticated
        and user.groups.filter(name=TEACHER_GROUP_NAME).exists()
    )

def login_redirect_url_for_user(user: AbstractUser | None) -> str:
    """
    Return the frontend a user should land on after login depending on their role.

    Teachers (members of the ``Teacher`` Django group) are sent to the teacher
    frontend, everyone else (students) to the gamification dashboard.
    """
    return TEACHER_REDIRECT_URL if is_teacher(user) else STUDENT_REDIRECT_URL

@login_required
def post_login_redirect(request: HttpRequest) -> HttpResponse:
    """
    Redirect the logged-in user to the frontend matching their role.

    Used by the single page app after a headless API login, where no server-side
    login redirect happens. Unauthenticated visitors are sent to the login page.
    """
    return redirect(login_redirect_url_for_user(request.user))

def serve_teacher_frontend(request: HttpRequest, path: str | None = None) -> HttpResponse:
    """
    Serve the teacher frontend entry point, restricted to teachers.

    Anonymous visitors are sent to the login page, authenticated non-teachers
    (e.g. students) are redirected to their own dashboard. Superusers may always
    access it. This guards the page itself; in production the same restriction
    must be enforced by whatever serves the static files (e.g. the web server).
    """
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    if not (is_teacher(request.user) or request.user.is_superuser):
        return redirect(STUDENT_REDIRECT_URL)

    document_root = f"{settings.BASE_DIR}/frontend/teacher/dist/openbook/teacher"
    return serve(request, path=path or "index.html", document_root=document_root)
