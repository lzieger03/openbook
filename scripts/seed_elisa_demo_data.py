from __future__ import annotations

import os
import sys
from decimal import Decimal
from pathlib import Path
from uuid import UUID


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

sys.path.insert(0, str(SRC_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openbook.settings")

import django

django.setup()

from allauth.account.models import EmailAddress
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.utils import timezone

from openbook.auth.models import Group
from openbook.auth.models import Role
from openbook.auth.models import RoleAssignment
from openbook.auth.models import User
from openbook.content.models import Course
from openbook.content.models import CourseMaterial
from openbook.content.models import LibraryGroup
from openbook.content.models import Textbook
from openbook.content.models import TextbookPage
from openbook.gamification.models import AccountProgress
from openbook.gamification.models import AccountStreak
from openbook.gamification.models import CourseProgress
from openbook.gamification.models import Skill
from openbook.gamification.models import SkillProgress


PASSWORD = "openbook"
COURSE_ID = UUID("48f16b3c-1856-4187-8343-09e4263f16cd")


def upsert_user(username: str, email: str, first_name: str, last_name: str, group: Group) -> User:
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True,
        },
    )
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.is_active = True
    user.set_password(PASSWORD)
    user.save()
    user.groups.add(group)
    EmailAddress.objects.update_or_create(
        user=user,
        email=user.email,
        defaults={"verified": True, "primary": True},
    )
    return user


def upsert_course_group(teacher: User) -> LibraryGroup:
    group, _ = LibraryGroup.objects.get_or_create(
        slug="elisa-demo",
        parent=None,
        defaults={
            "name": "ELISA Demo",
            "description": "Lokale Testdaten fuer das ELISA-Benutzerhandbuch.",
            "text_format": "MD",
            "created_by": teacher,
            "modified_by": teacher,
        },
    )
    group.name = "ELISA Demo"
    group.description = "Lokale Testdaten fuer das ELISA-Benutzerhandbuch."
    group.text_format = "MD"
    group.created_by = group.created_by or teacher
    group.modified_by = teacher
    group.save()
    return group


def upsert_course(group: LibraryGroup, teacher: User) -> Course:
    course, _ = Course.objects.get_or_create(
        id=COURSE_ID,
        defaults={
            "name": "KI Grundlagen",
            "slug": "ki-grundlagen",
            "description": "Demo-Kurs mit Inhalten fuer Dashboard, Chat, Quiz, Exam und Spiele.",
            "text_format": "MD",
            "group": group,
            "owner": teacher,
            "created_by": teacher,
            "modified_by": teacher,
            "is_template": False,
        },
    )
    course.name = "KI Grundlagen"
    course.slug = "ki-grundlagen"
    course.description = "Demo-Kurs mit Inhalten fuer Dashboard, Chat, Quiz, Exam und Spiele."
    course.text_format = "MD"
    course.group = group
    course.owner = teacher
    course.created_by = teacher
    course.modified_by = teacher
    course.is_template = False
    course.save()
    return course


def upsert_skills(course: Course) -> list[Skill]:
    skill_specs = [
        ("Prompting", "Zielfuehrende Fragen an ELISA formulieren."),
        ("Neuronale Netze", "Grundbegriffe von Gewichten, Training und Ausgabe verstehen."),
        ("Evaluation", "KI-Antworten kritisch pruefen und mit Quellen abgleichen."),
    ]
    skills = []

    for name, description in skill_specs:
        skill, _ = Skill.objects.get_or_create(name=name, defaults={"description": description})
        skill.description = description
        skill.save()
        skills.append(skill)

    course.skills.set(skills)
    return skills


def upsert_textbook(group: LibraryGroup, teacher: User) -> Textbook:
    textbook, _ = Textbook.objects.get_or_create(
        group=group,
        slug="ki-grundlagen-skript",
        defaults={
            "name": "KI Grundlagen Skript",
            "description": "Kurzes Demo-Skript fuer ELISA-Screenshots.",
            "text_format": "MD",
            "created_by": teacher,
            "modified_by": teacher,
        },
    )
    textbook.name = "KI Grundlagen Skript"
    textbook.description = "Kurzes Demo-Skript fuer ELISA-Screenshots."
    textbook.text_format = "MD"
    textbook.created_by = textbook.created_by or teacher
    textbook.modified_by = teacher
    textbook.save()
    return textbook


def upsert_pages(textbook: Textbook, skills: list[Skill], teacher: User) -> list[TextbookPage]:
    pages = [
        (
            1,
            "Einordnung von KI",
            """# Einordnung von KI

**Kuenstliche Intelligenz** beschreibt Systeme, die Aufgaben loesen, fuer die
normalerweise menschliches Denken noetig waere. Im Kurs unterscheiden wir
regelbasierte Systeme, maschinelles Lernen und generative KI.

- Daten
- Modell
- Training
- Inferenz

`Prompting` hilft, eine Aufgabe klar zu formulieren und gute Antworten zu erhalten.
""",
            [skills[0]],
        ),
        (
            2,
            "Neuronale Netze",
            """# Neuronale Netze

Ein **Neuronales Netz** besteht aus Schichten, Gewichten und Aktivierungsfunktionen.
Beim Training werden Gewichte so angepasst, dass die Ausgabe besser zur Zielantwort
passt.

## Wichtige Begriffe

**Gewichte** steuern, wie stark ein Eingangssignal wirkt. **Bias** verschiebt die
Aktivierung. Die **Loss-Funktion** misst den Fehler.
""",
            [skills[1]],
        ),
        (
            3,
            "Gute Prompts",
            """# Gute Prompts

Ein guter Prompt nennt Kontext, Ziel und gewuenschtes Ausgabeformat. Statt "Erklaere
alles" ist eine konkrete Frage besser.

## Beispiel

**Rolle:** Lerncoach. **Ziel:** Drei Verstaendnisfragen erzeugen. **Format:**
Nummerierte Liste.
""",
            [skills[0], skills[2]],
        ),
        (
            4,
            "Antworten bewerten",
            """# Antworten bewerten

KI-Antworten koennen plausibel klingen und trotzdem falsch sein. Vergleichen Sie
wichtige Aussagen mit dem Skript, mit Quellen und mit Rueckmeldungen der Lehrperson.

## Prueffragen

- Passt die Antwort zur Aufgabe?
- Nennt sie Annahmen?
- Gibt es Widersprueche im Kursmaterial?
""",
            [skills[2]],
        ),
    ]

    created_pages = []
    for position, title, source, page_skills in pages:
        page, _ = TextbookPage.objects.get_or_create(
            textbook=textbook,
            parent=None,
            position=position,
            defaults={
                "name": title,
                "description": "Demo-Seite fuer ELISA.",
                "text_format": "MD",
                "content": {
                    "type": "source",
                    "format": "MD",
                    "source": source,
                    "filename": "ki-grundlagen-demo.md",
                },
                "created_by": teacher,
                "modified_by": teacher,
            },
        )
        page.name = title
        page.description = "Demo-Seite fuer ELISA."
        page.text_format = "MD"
        page.content = {
            "type": "source",
            "format": "MD",
            "source": source,
            "filename": "ki-grundlagen-demo.md",
        }
        page.created_by = page.created_by or teacher
        page.modified_by = teacher
        page.save()
        page.skills.set(page_skills)
        created_pages.append(page)

    return created_pages


def upsert_material(course: Course, textbook: Textbook, teacher: User) -> CourseMaterial:
    material = CourseMaterial.objects.filter(course=course, textbook=textbook).first()

    if material is None:
        used_positions = set(
            CourseMaterial.objects.filter(course=course).values_list("position", flat=True)
        )
        position = 1
        while position in used_positions:
            position += 1

        material = CourseMaterial.objects.create(
            course=course,
            textbook=textbook,
            position=position,
            created_by=teacher,
            modified_by=teacher,
        )
    else:
        material.modified_by = teacher
        material.save()

    return material


def upsert_roles(course: Course, teacher: User) -> tuple[Role, Role]:
    course_type = ContentType.objects.get_for_model(Course)

    student_role, _ = Role.objects.get_or_create(
        scope_type=course_type,
        scope_uuid=course.id,
        slug="student",
        defaults={
            "name": "Student",
            "description": "Enrolled student of this course.",
            "text_format": "MD",
            "priority": 0,
            "created_by": teacher,
            "modified_by": teacher,
        },
    )
    student_role.name = "Student"
    student_role.description = "Enrolled student of this course."
    student_role.text_format = "MD"
    student_role.priority = 0
    student_role.is_active = True
    student_role.modified_by = teacher
    student_role.save()

    teacher_role, _ = Role.objects.get_or_create(
        scope_type=course_type,
        scope_uuid=course.id,
        slug="teacher",
        defaults={
            "name": "Teacher",
            "description": "Teacher of this course.",
            "text_format": "MD",
            "priority": 2,
            "created_by": teacher,
            "modified_by": teacher,
        },
    )
    teacher_role.name = "Teacher"
    teacher_role.description = "Teacher of this course."
    teacher_role.text_format = "MD"
    teacher_role.priority = 2
    teacher_role.is_active = True
    teacher_role.modified_by = teacher
    teacher_role.save()

    return student_role, teacher_role


def upsert_assignment(course: Course, role: Role, user: User, teacher: User) -> None:
    course_type = ContentType.objects.get_for_model(Course)
    RoleAssignment.objects.get_or_create(
        scope_type=course_type,
        scope_uuid=course.id,
        role=role,
        user=user,
        defaults={
            "assignment_method": RoleAssignment.AssignmentMethod.MANUAL,
            "start_date": timezone.now(),
            "created_by": teacher,
            "modified_by": teacher,
        },
    )


def upsert_progress(student: User, teacher: User, course: Course, skills: list[Skill]) -> None:
    AccountProgress.objects.update_or_create(
        account=student,
        defaults={"point_total": 180, "level": 3},
    )
    AccountProgress.objects.update_or_create(
        account=teacher,
        defaults={"point_total": 0, "level": 1},
    )
    AccountStreak.objects.update_or_create(
        account=student,
        defaults={
            "current_streak": 4,
            "longest_streak": 7,
            "last_active_date": timezone.localdate(),
            "last_active_at": timezone.now(),
            "streak_freezes": 1,
        },
    )
    CourseProgress.objects.update_or_create(
        account=student,
        course=course,
        defaults={
            "course_points": 120,
            "course_level": 2,
            "course_progress": Decimal("35.00"),
        },
    )

    for index, skill in enumerate(skills, start=1):
        SkillProgress.objects.update_or_create(
            account=student,
            skill=skill,
            defaults={"level": index, "progress": Decimal(str(25 * index))},
        )


def main() -> None:
    management.call_command("load_initial_data", verbosity=0)

    student_group = Group.objects.get(name="Student")
    teacher_group = Group.objects.get(name="Teacher")

    student = upsert_user(
        username="student.demo",
        email="student.demo@example.local",
        first_name="Maya",
        last_name="Student",
        group=student_group,
    )
    teacher = upsert_user(
        username="teacher.demo",
        email="teacher.demo@example.local",
        first_name="Tobias",
        last_name="Teacher",
        group=teacher_group,
    )

    group = upsert_course_group(teacher)
    course = upsert_course(group, teacher)
    skills = upsert_skills(course)
    textbook = upsert_textbook(group, teacher)
    pages = upsert_pages(textbook, skills, teacher)
    material = upsert_material(course, textbook, teacher)
    student_role, teacher_role = upsert_roles(course, teacher)

    upsert_assignment(course, student_role, student, teacher)
    upsert_assignment(course, teacher_role, teacher, teacher)
    upsert_progress(student, teacher, course, skills)

    print("ELISA test data ready")
    print(f"student: {student.username} / {PASSWORD}")
    print(f"teacher: {teacher.username} / {PASSWORD}")
    print(f"course: {course.id} {course.name}")
    print(f"textbook pages: {len(pages)}")
    print(f"material: {material.id}")


if __name__ == "__main__":
    main()
