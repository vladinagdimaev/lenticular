# Lenticular — Django catalog management

Django Admin: categories, subcategories, products, multiple media uploads, precise dimensions, prices and stock per variant.

## Local setup

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
python manage.py makemigrations catalog
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ and manage products. Public JSON endpoint: /api/catalog/.

## Production
Deploy as a **separate Render web service** with root directory `backend`, build command `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`, start command `gunicorn config.wsgi:application`. Configure DJANGO_SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DATABASE_URL. **Configure persistent S3-compatible storage before real uploads**: Render's default local filesystem is ephemeral. Create the initial superuser securely via shell or a one-time management command, not in the repository.

The existing root-level static site is intentionally unchanged. The API is read-only and exposes only active products with in-stock variants. Payments are not implemented.
