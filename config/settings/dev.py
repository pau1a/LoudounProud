"""Development settings."""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Use local PostgreSQL with peer/trust auth by default
DATABASES["default"].update({  # noqa: F405
    "NAME": os.getenv("DB_NAME", "loudounproud"),  # noqa: F405
    "USER": os.getenv("DB_USER", "paula"),  # noqa: F405
    "PASSWORD": os.getenv("DB_PASSWORD", ""),  # noqa: F405
    "HOST": os.getenv("DB_HOST", "localhost"),  # noqa: F405
})

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
