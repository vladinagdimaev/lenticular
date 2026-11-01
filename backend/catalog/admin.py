from django.contrib import admin
from .models import Category, Subcategory, Product, ProductMedia, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}

class MediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1

class VariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "title", "subcategory", "active", "created_at")
    list_filter = ("active", "subcategory__category", "subcategory")
    search_fields = ("sku", "title", "description")
    list_editable = ("active",)
    inlines = (VariantInline, MediaInline)
    list_per_page = 50
