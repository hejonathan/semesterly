"""Settings for the Render + Neon deployment (copied into semesterly/ at build time)."""
import os
import sys
from urllib.parse import urlparse, parse_qs

DEBUG = False
SHOW_DEBUG_TOOLBAR = False

_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
ALLOWED_HOSTS = [_host, "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://" + _host]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# DATABASE_URL comes from Neon, e.g. postgresql://user:pw@host/db?sslmode=require
_db = urlparse(os.environ.get("DATABASE_URL", "postgresql://build:build@localhost/build"))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _db.path.lstrip("/"),
        "USER": _db.username,
        "PASSWORD": _db.password,
        "HOST": _db.hostname,
        "PORT": _db.port or 5432,
        "OPTIONS": {"sslmode": parse_qs(_db.query).get("sslmode", ["require"])[0]},
        "CONN_MAX_AGE": 60,
    }
}

# Don't email error reports to the Semester.ly team (the SMTP attempt also
# hangs the worker until Render kills it).
ADMINS = []
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Serve static files from the app itself with WhiteNoise.
STATIC_ROOT = "/code/staticfiles"

# Adjust middleware defined earlier in settings.py:
#  - add WhiteNoise for static files
#  - always treat requests as JHU (the stock middleware infers the school from
#    the subdomain, which doesn't work on *.onrender.com)
_base = sys.modules["semesterly.settings"].MIDDLEWARE
MIDDLEWARE = ("whitenoise.middleware.WhiteNoiseMiddleware",) + tuple(
    "selfhost_middleware.ForceJHUMiddleware"
    if m == "semesterly.middleware.subdomain_middleware.SubdomainMiddleware"
    else m
    for m in _base
)

# Show the "student self-hosted version" popup.
import copy  # noqa: E402

TEMPLATES = copy.deepcopy(sys.modules["semesterly.settings"].TEMPLATES)
TEMPLATES[0]["OPTIONS"]["context_processors"].append("selfhost_middleware.selfhost_context")

# settings.py initialises Rollbar with the official Semester.ly token whenever
# DEBUG is False. Disable it so this instance doesn't report errors to them.
import rollbar  # noqa: E402

rollbar.init = lambda *args, **kwargs: None
