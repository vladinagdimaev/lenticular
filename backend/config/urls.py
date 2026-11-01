from django.contrib import admin
from django.urls import path, include
from catalog.views import catalog_json

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/catalog/", catalog_json, name="catalog-json"),
]
