# OpenBook: Interactive Online Textbooks - Server
# © 2026 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Ledejna Salihi (@LedejnaSalihi)
# Lars Zieger (@lzieger03)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

"""One-shot seed command to make the website fully testable on a fresh database.

Running ``manage.py seed_demo`` brings the database from "empty" to "ready to
click through the whole app" in a single step. It is **idempotent**: re-running
never creates duplicates, it only fills in what is missing.

It orchestrates the existing building blocks and adds the glue that ties them
into a usable end-to-end demo:

1. ``migrate``                     – make sure the schema exists.
2. ``load_initial_data``           – site, languages, auth config, groups,
                                     library groups and the demo course + roles.
3. ``load_gamification_dummy_data`` – demo learners, skills, level thresholds,
                                     account/skill/course progress and streaks.
4. A login-able **superuser** (admin area) and a **teacher** account.
5. **Group membership** so learners/teachers carry the right model permissions.
6. **Enrollment** of the demo learners into the demo course (role assignments).
7. A **textbook with real pages + course material** so the content reader and
   the chat/quiz context actually have something to show.
8. **Skills wired to the course and its pages** so the dashboard cards and the
   quiz → skill point flow light up.

At the end it prints the credentials you can log in with.
"""

from __future__ import annotations

from django.contrib.auth         import get_user_model
from django.core                 import management
from django.core.management.base import BaseCommand
from django.db                   import IntegrityError, transaction
from django.utils.timezone       import now

from openbook.auth.models     import Group, Role, RoleAssignment
from openbook.content.models  import Course, CourseMaterial, Textbook, TextbookPage
from openbook.core.management.commands.load_initial_data import Command as LoadInitialData
from openbook.gamification.models import Skill


# The demo course shipped by the ``openbook_content/courses`` fixture.
COURSE_PK = "3629d56b-e3ae-41c9-8438-0046e057a69b"

# Learners created by ``load_gamification_dummy_data`` (kept in sync on purpose).
DEMO_LEARNER_USERNAMES = ["max.mustermann", "jane.doe", "demo.user"]

# Login accounts created here (password is the same for every demo account).
DEMO_PASSWORD = "password"

SUPERUSER = {
    "username":   "admin",
    "email":      "admin@example.com",
    "first_name": "Admin",
    "last_name":  "Istrator",
    "password":   "admin",
}

TEACHER = {
    "username":   "teacher.demo",
    "email":      "teacher@example.com",
    "first_name": "Tina",
    "last_name":  "Teacher",
    "password":   DEMO_PASSWORD,
}

# Textbook content authored for the demo course. Each page is plain Markdown so
# it renders directly in the learner content reader.
TEXTBOOK = {
    "name":        "Web Development Basics",
    "slug":        "web-development-basics",
    "description": "A short hands-on introduction to building for the web.",
}

PAGES = [
    {
        "name":   "Introduction",
        "skills": ["Problem Solving"],
        "source": (
            "# Welcome to Web Development\n\n"
            "This short textbook walks you through the three pillars of the web: "
            "**HTML** for structure, **CSS** for presentation and "
            "**JavaScript** for behaviour.\n\n"
            "Work through the pages in order and use the tutor chat whenever you "
            "get stuck.\n\n"
            "> Tip: every page can be downloaded as a PDF from the reader.\n"
        ),
    },
    {
        "name":   "HTML: Structure",
        "skills": ["Problem Solving", "Persistence"],
        "source": (
            "# HTML: The Structure of a Page\n\n"
            "HTML (HyperText Markup Language) describes **what** content a page "
            "contains using *elements*.\n\n"
            "```html\n"
            "<!DOCTYPE html>\n"
            "<html lang=\"en\">\n"
            "  <head>\n"
            "    <title>My first page</title>\n"
            "  </head>\n"
            "  <body>\n"
            "    <h1>Hello, world!</h1>\n"
            "    <p>This is a paragraph.</p>\n"
            "  </body>\n"
            "</html>\n"
            "```\n\n"
            "## Key elements\n\n"
            "- `<h1>`–`<h6>` — headings\n"
            "- `<p>` — paragraphs\n"
            "- `<a>` — links\n"
            "- `<ul>` / `<ol>` / `<li>` — lists\n"
        ),
    },
    {
        "name":   "CSS: Presentation",
        "skills": ["Problem Solving"],
        "source": (
            "# CSS: Making It Look Good\n\n"
            "CSS (Cascading Style Sheets) controls **how** the content looks.\n\n"
            "```css\n"
            "body {\n"
            "  font-family: system-ui, sans-serif;\n"
            "  line-height: 1.6;\n"
            "  color: #111;\n"
            "}\n\n"
            "h1 {\n"
            "  color: rebeccapurple;\n"
            "}\n"
            "```\n\n"
            "Selectors target elements, and declarations set their properties. "
            "Practice by changing the colours above.\n"
        ),
    },
    {
        "name":   "JavaScript: Behaviour",
        "skills": ["Problem Solving", "Persistence", "Collaboration"],
        "source": (
            "# JavaScript: Adding Behaviour\n\n"
            "JavaScript makes pages **interactive**.\n\n"
            "```js\n"
            "const button = document.querySelector(\"button\");\n"
            "button.addEventListener(\"click\", () => {\n"
            "  alert(\"You clicked the button!\");\n"
            "});\n"
            "```\n\n"
            "## What to try next\n\n"
            "1. Read the content again and take the quiz.\n"
            "2. Ask the tutor to explain anything that is unclear.\n"
            "3. Mark the course complete to earn your points.\n"
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the database with everything needed to test the website locally."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--skip-migrate",
            action="store_true",
            help="Do not run database migrations before seeding.",
        )

    def handle(self, *args, **options):
        if not options.get("skip_migrate"):
            self.stdout.write(self.style.MIGRATE_HEADING("Applying migrations…"))
            management.call_command("migrate", verbosity=1)

        self.stdout.write(self.style.MIGRATE_HEADING("Loading initial fixtures…"))
        self._load_fixtures()

        self.stdout.write(self.style.MIGRATE_HEADING("Loading gamification demo data…"))
        management.call_command("load_gamification_dummy_data", verbosity=1)

        # Everything below is the glue that turns the loaded data into a usable,
        # clickable demo. Wrapped in a transaction so a partial seed never sticks.
        with transaction.atomic():
            self._ensure_superuser()
            teacher = self._ensure_teacher()
            learners = self._add_learners_to_group()
            course = self._get_course()
            if course is not None:
                self._enroll_in_course(course, learners, teacher)
                textbook = self._ensure_textbook(course)
                self._ensure_pages(textbook)
                self._ensure_course_material(course, textbook)
                self._wire_course_skills(course)

        self._print_summary(course)

    # -- Fixtures ---------------------------------------------------------------

    def _load_fixtures(self) -> None:
        """Load the initial-data fixtures one by one, tolerating already-loaded ones.

        ``load_initial_data`` aborts the whole run if a single fixture clashes
        with rows already present (e.g. the anonymous-permission unique
        constraint on a re-seeded database). Loading each fixture in its own call
        and skipping the ones that are already present keeps ``seed_demo``
        idempotent on both fresh and existing databases.
        """
        for fixture in LoadInitialData.FIXTURES:
            try:
                management.call_command("loaddata", fixture, verbosity=0)
                self.stdout.write(f"Loaded fixture: {fixture}")
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f"Fixture already present, skipping: {fixture}"))

    # -- Accounts ---------------------------------------------------------------

    def _ensure_superuser(self):
        """Create a login-able admin account for the Django/admin + teacher area."""
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=SUPERUSER["username"],
            defaults={
                "email":        SUPERUSER["email"],
                "first_name":   SUPERUSER["first_name"],
                "last_name":    SUPERUSER["last_name"],
                "is_staff":     True,
                "is_superuser": True,
            },
        )

        # Always make sure the flags and a known password are in place, even if
        # the account already existed with different settings.
        user.is_staff = True
        user.is_superuser = True
        user.set_password(SUPERUSER["password"])
        user.save()

        self.stdout.write(("Created" if created else "Updated") + f" superuser: {user.username}")
        return user

    def _ensure_teacher(self):
        """Create a teacher account in the Teacher group with a known password."""
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=TEACHER["username"],
            defaults={
                "email":      TEACHER["email"],
                "first_name": TEACHER["first_name"],
                "last_name":  TEACHER["last_name"],
                "is_staff":   True,
            },
        )

        user.is_staff = True
        user.set_password(TEACHER["password"])
        user.save()

        self._add_to_group(user, "Teacher")
        self.stdout.write(("Created" if created else "Updated") + f" teacher: {user.username}")
        return user

    def _add_learners_to_group(self):
        """Put the gamification demo learners in the Student group + set a password."""
        User = get_user_model()
        learners = list(User.objects.filter(username__in=DEMO_LEARNER_USERNAMES))

        for user in learners:
            # The gamification command already sets "password" on creation, but
            # set it again so existing accounts are guaranteed to be log-in-able.
            user.set_password(DEMO_PASSWORD)
            user.save()
            self._add_to_group(user, "Student")
            self.stdout.write(f"Learner in Student group: {user.username}")

        return learners

    def _add_to_group(self, user, group_name: str) -> None:
        """Add the user to the named group if it exists (groups come from fixtures).

        Uses the project's own ``openbook_auth.Group`` because ``User.groups``
        points at that model, not Django's base ``auth.Group``.
        """
        group = Group.objects.filter(name=group_name).first()
        if group is not None:
            user.groups.add(group)

    # -- Course, enrollment & content ------------------------------------------

    def _get_course(self):
        course = Course.objects.filter(pk=COURSE_PK).first() or Course.objects.first()
        if course is None:
            self.stdout.write(self.style.WARNING(
                "No course found — skipping enrollment and content seeding."
            ))
        return course

    def _enroll_in_course(self, course, learners, teacher) -> None:
        """Give learners the course's Student role and the teacher its Teacher role."""
        student_role = Role.objects.filter(scope_uuid=course.id, slug="student").first()
        teacher_role = Role.objects.filter(scope_uuid=course.id, slug="teacher").first()

        if student_role is not None:
            for user in learners:
                if self._assign_role(student_role, user):
                    self.stdout.write(f"Enrolled {user.username} as Student in {course.name}")

        if teacher_role is not None and teacher is not None:
            if self._assign_role(teacher_role, teacher):
                self.stdout.write(f"Assigned {teacher.username} as Teacher in {course.name}")

    def _assign_role(self, role: Role, user) -> bool:
        """Create a role assignment for the user, returning True if newly created.

        ``scope_type`` / ``scope_uuid`` are copied from the role explicitly: the
        model only derives them in ``clean()``, which ``save()`` does not run, so
        they would otherwise be NULL on a plain ``create``.
        """
        _, created = RoleAssignment.objects.get_or_create(
            role=role,
            user=user,
            defaults={
                "scope_type":        role.scope_type,
                "scope_uuid":        role.scope_uuid,
                "assignment_method": RoleAssignment.AssignmentMethod.MANUAL,
                "start_date":        now(),
            },
        )
        return created

    def _ensure_textbook(self, course) -> Textbook:
        """Create (once) a textbook in the course's library group."""
        textbook, created = Textbook.objects.get_or_create(
            group=course.group,
            slug=TEXTBOOK["slug"],
            defaults={
                "name":        TEXTBOOK["name"],
                "description": TEXTBOOK["description"],
                "text_format": "MD",
            },
        )
        self.stdout.write(("Created" if created else "Exists") + f" textbook: {textbook.name}")
        return textbook

    def _ensure_pages(self, textbook: Textbook) -> None:
        """Create the demo pages (idempotent on textbook + position) with content."""
        skills_by_name = {skill.name: skill for skill in Skill.objects.all()}

        for position, page_info in enumerate(PAGES):
            page, created = TextbookPage.objects.get_or_create(
                textbook=textbook,
                parent=None,
                position=position,
                defaults={
                    "name":        page_info["name"],
                    "text_format": "MD",
                    "content": {
                        "type":   "source",
                        "format": "MD",
                        "source": page_info["source"],
                    },
                },
            )

            # Wire the page's skills (so quiz points on this page advance them).
            page_skills = [skills_by_name[name] for name in page_info["skills"] if name in skills_by_name]
            if page_skills:
                page.skills.add(*page_skills)

            self.stdout.write(("Created" if created else "Exists") + f" page: {page.name}")

    def _ensure_course_material(self, course, textbook: Textbook) -> None:
        """Link the textbook into the course syllabus (no page range = whole book)."""
        material, created = CourseMaterial.objects.get_or_create(
            course=course,
            textbook=textbook,
            defaults={"position": 0},
        )
        self.stdout.write(("Created" if created else "Exists") + f" course material for {course.name}")

    def _wire_course_skills(self, course) -> None:
        """Attach the demo skills to the course so dashboard cards show them."""
        skills = list(Skill.objects.all())
        if skills:
            course.skills.add(*skills)
            self.stdout.write(f"Linked {len(skills)} skill(s) to {course.name}")

    # -- Summary ----------------------------------------------------------------

    def _print_summary(self, course) -> None:
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Seeding complete. You can now log in with:"))
        self.stdout.write("")
        self.stdout.write(f"  Admin    : {SUPERUSER['username']} / {SUPERUSER['password']}   (Django admin + teacher area)")
        self.stdout.write(f"  Teacher  : {TEACHER['username']} / {TEACHER['password']}   (teacher area)")
        for username in DEMO_LEARNER_USERNAMES:
            self.stdout.write(f"  Learner  : {username} / {DEMO_PASSWORD}   (dashboard)")
        self.stdout.write("")
        if course is not None:
            self.stdout.write(f"  Demo course: {course.name}  (id {course.id})")
        self.stdout.write("")
        self.stdout.write("Tip: log in as 'max.mustermann' to see a fully populated learner dashboard.")
