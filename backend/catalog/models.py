from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("שם קטגוריה", max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)
    order = models.PositiveIntegerField("סדר תצוגה", default=0)
    class Meta:
        ordering = ["order", "name"]
        verbose_name = "קטגוריה"
        verbose_name_plural = "קטגוריות"
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="subcategories", verbose_name="קטגוריה")
    name = models.CharField("שם תת־קטגוריה", max_length=100)
    slug = models.SlugField(allow_unicode=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["category", "slug"], name="unique_subcategory_slug")]
        verbose_name = "תת־קטגוריה"
        verbose_name_plural = "תתי־קטגוריות"
    def __str__(self):
        return f"{self.category} / {self.name}"

class Product(models.Model):
    title = models.CharField("שם היצירה", max_length=200)
    sku = models.CharField("מק״ט", max_length=64, unique=True)
    description = models.TextField("תיאור", blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="products", verbose_name="תת־קטגוריה")
    active = models.BooleanField("מוצג באתר", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "מוצר"
        verbose_name_plural = "מוצרים"
    def __str__(self):
        return f"{self.sku} — {self.title}"

class ProductMedia(models.Model):
    class Kind(models.TextChoices):
        IMAGE = "image", "תמונה / GIF"
        VIDEO = "video", "וידאו"
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="media", verbose_name="מוצר")
    file = models.FileField("קובץ", upload_to="products/%Y/%m/")
    kind = models.CharField("סוג מדיה", max_length=10, choices=Kind.choices, default=Kind.VIDEO)
    alt_text = models.CharField("תיאור נגיש", max_length=250, blank=True)
    order = models.PositiveIntegerField("סדר", default=0)
    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "מדיה"
        verbose_name_plural = "מדיה"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", verbose_name="מוצר")
    width_cm = models.DecimalField("רוחב בס״מ", max_digits=6, decimal_places=1)
    height_cm = models.DecimalField("גובה בס״מ", max_digits=6, decimal_places=1)
    price_ils = models.DecimalField("מחיר בש״ח", max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField("כמות במלאי", default=0)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["product", "width_cm", "height_cm"], name="unique_product_dimensions")]
        verbose_name = "מידה ומלאי"
        verbose_name_plural = "מידות ומלאי"
    def __str__(self):
        return f"{self.width_cm}×{self.height_cm} ס״מ — {self.stock} במלאי"
