import sys

from .settings import *

SECRET_KEY = env("SECRET_KEY")
DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("PGDATABASE"),
        "USER": env("PGUSER"),
        "PASSWORD": env("PGPASSWORD"),
        "HOST": env("PGHOST"),
        "PORT": env("PGPORT"),
        "OPTIONS": {
            "pool": True,
        },
    }
}

# SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "ERROR",  # Nur Fehler ausgeben
            "class": "logging.StreamHandler",
            "stream": sys.stderr,  # Schreibe auf stderr
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  # Setze das Log-Level
            "propagate": True,
        },
    },
}
