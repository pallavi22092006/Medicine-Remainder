# MediRemind — Django Edition

Same multi-user medicine reminder system, rebuilt in Python/Django:
Django + Django REST Framework for the API, JWT auth via
`djangorestframework-simplejwt`, and Django's built-in SQLite database
(Python's SQLite support ships with the language — no compiler, no
native modules, no Visual Studio needed on Windows).

## What it does

- **Sign up / log in** with name, email, phone, password (Django hashes
  passwords automatically with PBKDF2)
- **Reminders**: each user manages their own medicine name, dosage, time,
  frequency (Once / Daily / Weekly / As Needed), and a customizable alarm
  tone (Chime, Beep, Urgent, Bell)
- **In-browser alarm**: when a reminder's time hits, a full-screen alert
  rings a synthesized tone (Web Audio API — no sound files needed) until
  you Mark as Taken, Snooze, or Dismiss it, plus a backup desktop
  notification
- **Django admin** at `/admin/` to inspect users and reminders directly

## Project structure

```
medireminder-django/
├── manage.py
├── requirements.txt
├── .env.example
├── medireminder/          # project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── reminders/             # the app: models, API, admin
│   ├── models.py           # User (custom) + Reminder
│   ├── managers.py         # email-based user manager
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── templates/
    └── index.html          # frontend (login/signup + dashboard + alarms)
```

## Setup

Requires **Python 3.10+**. Check with `python --version` (or `python3 --version`
on Mac/Linux).

```bash
cd medireminder-django

# Create a virtual environment (keeps dependencies isolated)
python -m venv venv

# Activate it:
#   Windows:      venv\Scripts\activate
#   Mac/Linux:    source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env   # Windows: copy .env.example .env
```

Open `.env` and set `DJANGO_SECRET_KEY` to a long random string. You can
generate one with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Create the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

(Optional) Create an admin account to log into `/admin/`:
```bash
python manage.py createsuperuser
```

## Run

```bash
python manage.py runserver
```

Visit **http://localhost:8000** — sign up, log in, and add a reminder with
a time a minute or two away to see the alarm fire.

## API reference

| Method | Endpoint                  | Auth | Body                                                |
|--------|----------------------------|------|-------------------------------------------------------|
| POST   | /api/auth/register/        | No   | `{ name, email, phone, password }`                    |
| POST   | /api/auth/login/           | No   | `{ email, password }`                                 |
| GET    | /api/reminders/             | Yes  | —                                                       |
| POST   | /api/reminders/             | Yes  | `{ medicine_name, dosage, time, frequency, alarm_sound }` |
| PUT    | /api/reminders/<id>/        | Yes  | any of the above fields, or `{ taken: true }`         |
| DELETE | /api/reminders/<id>/        | Yes  | —                                                       |

Auth requests use header: `Authorization: Bearer <access_token>`

## Scaling notes for 500+ users

- SQLite handles this app's traffic pattern (small, infrequent reads/writes)
  comfortably at this scale.
- To scale further or run multiple server processes, switch `DATABASES` in
  `settings.py` to PostgreSQL (`django.db.backends.postgresql`) — Django's
  ORM means your models and views don't need to change at all.
- Deploy with `gunicorn` or `uwsgi` behind Nginx, or on a platform like
  Render, Railway, or PythonAnywhere. Set `DJANGO_DEBUG=False` and a real
  `ALLOWED_HOSTS` list in production.
- For notifications that work even when the browser tab is closed (SMS,
  email, or push), add a scheduled job with Celery + Celery Beat, or a
  simple cron job calling a Django management command that checks due
  reminders and sends via Twilio (SMS) or Django's email backend.

## Security notes already built in

- Passwords hashed by Django's built-in password hashers, never stored
  in plain text
- JWT access tokens expire after 30 days (adjust `SIMPLE_JWT` in
  `settings.py`)
- Every reminder query is filtered by the logged-in user, so no one can
  see or modify another user's data
- Django's built-in CSRF and security middleware are enabled by default
