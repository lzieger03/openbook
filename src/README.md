OpenBook Server
===============

This is the server part of OpenBook. For all practical purposes this is a pretty much standard
Django web application, with the notable difference that Django channels is used for real-time
communication over websockets. So an ASGI-capable web server is needed to host the platform.
See README files at the root-level of the project for more information.

Seeding demo data
-----------------

To get a database you can actually click through (login users, a demo course with readable
content, skills, level thresholds, gamification progress and enrollments), run the seed command:

```sh
python manage.py seed_demo
```

The command lives in [`openbook/core/management/commands/seed_demo.py`](openbook/core/management/commands/seed_demo.py).
It runs the migrations, loads the initial fixtures and gamification demo data, and then wires
everything together into a fully testable demo. It is **idempotent** — running it again only fills
in what is missing and never creates duplicates, so it is safe on both a fresh and an existing
database. Pass `--skip-migrate` to skip running migrations.

Afterwards you can log in with:

| Role    | Username         | Password   | Where                         |
|---------|------------------|------------|-------------------------------|
| Admin   | `admin`          | `admin`    | Django admin + teacher area   |
| Teacher | `teacher.demo`   | `password` | teacher area                  |
| Learner | `max.mustermann` | `password` | dashboard (fully populated)   |
| Learner | `jane.doe`       | `password` | dashboard                     |
| Learner | `demo.user`      | `password` | dashboard                     |

> These are throwaway credentials for local testing only — never use this data on a public server.
