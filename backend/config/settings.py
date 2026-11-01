import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-before-deploy")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = [x.strip() for x in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if x.strip()]
CSRF_TRUSTED_ORIGINS = [x.strip() for x in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if x.strip()]
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "catalog",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates",
              "DIRS": [], "APP_DIRS": True,
              "OPTIONS": {"context_processors": [
                  "django.template.context_processors.debug",
                  "django.template.context_processors.request",
                  "django.contrib.auth.context_processors.auth",
                  "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": dj_database_url.config(default="sqlite:///" + str(BASE_DIR / "db.sqlite3"), conn_max_age=600, conn_health_checks=True)}
LANGUAGE_CODE = "he"
TIME_ZONE = "Asia/Jerusalem"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STORAGES = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}}
if os.environ.get("AWS_STORAGE_BUCKET_NAME"):
    STORAGES["default"] = {"BACKEND": "storages.backends.s3.S3Storage", "OPTIONS": {"bucket_name": os.environ.get("AWS_STORAGE_BUCKET_NAME") or "lenticular-media", "endpoint_url": os.environ.get("AWS_S3_ENDPOINT_URL", "https://br-broad-shape-b9rffuff.storage.c-7.eu-central-1.aws.neon.tech"), "region_name": "eu-central-1", "addressing_style": "path", "querystring_auth": False}}
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_REGION_NAME = "eu-central-1"
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = None
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False}},
}
