"""One-time initial admin creation; reads credentials from Render environment."""
import os
from django.conf import settings
from django.db import migrations


def create_initial_admin(apps, schema_editor):
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    if not all((username, email, password)):
        return
    User = apps.get_model(settings.AUTH_USER_MODEL)
    if User.objects.using(schema_editor.connection.alias).filter(username=username).exists():
        return
    User.objects.using(schema_editor.connection.alias).create(
        username=username, email=email, is_staff=True, is_superuser=True,
        is_active=True, password="!",
    )
    # Historical migration models do not expose set_password; use Django's hasher.
    from django.contrib.auth.hashers import make_password
    User.objects.using(schema_editor.connection.alias).filter(username=username).update(
        password=make_password(password)
    )


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [migrations.RunPython(create_initial_admin, migrations.RunPython.noop)]
