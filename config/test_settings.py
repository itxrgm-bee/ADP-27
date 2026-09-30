from .settings import *
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "test.sqlite3"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
ATTENDANCE_ALLOWED_IPS = ["203.0.113.10"]
TRUSTED_PROXY_IPS = ["127.0.0.1"]
