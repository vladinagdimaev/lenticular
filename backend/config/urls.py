from django.contrib import admin
from django.urls import path, include
from catalog.views import catalog_json
from catalog.studio import studio

urlpatterns = [
    path("admin/", admin.site.urls),
    path("studio/", studio, name="studio"),
    path("api/catalog/", catalog_json, name="catalog-json"),
]
