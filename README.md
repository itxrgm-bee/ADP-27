# Employee Attendance Management System

Django REST Framework backend with JWT authentication, PostgreSQL, a template dashboard, immutable attendance records, audit logs, holidays, and PDF reports.

## Local setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py makemigrations accounts attendance holidays
python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --noinput
python manage.py runserver
```

API documentation is available at `/api/docs/`. Employee login is `/api/auth/login/`; attendance actions alone require the source IP to be in `ATTENDANCE_ALLOWED_IPS`. The proxy must be the only host able to reach Django directly, and `TRUSTED_PROXY_IPS` must contain only that proxy's address. Set a strong `SECRET_KEY`, PostgreSQL `DATABASE_URL`, and real allowed hosts in production.

Manual attendance: `POST /api/admin/attendance/manual/` with `employee_id`, `date`, ISO `check_in`, optional ISO `check_out`, and `reason`. Existing attendance cannot be overwritten.

## Deployment

Copy `deployment/nginx.conf` to the Nginx sites directory, adjust `/opt/attendance`, install `deployment/attendance.service` into systemd, then run migrations and `collectstatic`. Gunicorn serves Django only on loopback; Nginx forwards the real client address using `X-Real-IP` and `X-Forwarded-For`.
