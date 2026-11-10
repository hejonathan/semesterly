import os

DEBUG = False
SHOW_DEBUG_TOOLBAR = False

ALLOWED_HOSTS = [os.environ["SITE_DOMAIN"]]
CSRF_TRUSTED_ORIGINS = ["https://" + os.environ["SITE_DOMAIN"]]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}

# settings.py initialises Rollbar with the official Semester.ly token whenever
# DEBUG is False. Disable it so this instance doesn't report errors to them.
import rollbar  # noqa: E402

rollbar.init = lambda *args, **kwargs: None
