from django.db import migrations, models
import django.db.models.deletion as deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Category", fields=[("id",models.BigAutoField(primary_key=True,serialize=False)),("name",models.CharField(max_length=100)),("slug",models.SlugField(unique=True,allow_unicode=True)),("order",models.PositiveIntegerField(default=0))],options={"ordering":["order","name"]}),
        migrations.CreateModel(name="Subcategory", fields=[("id",models.BigAutoField(primary_key=True,serialize=False)),("name",models.CharField(max_length=100)),("slug",models.SlugField(allow_unicode=True)),("category",models.ForeignKey(to="catalog.category",on_delete=deletion.PROTECT,related_name="subcategories"))]),
        migrations.CreateModel(name="Product", fields=[("id",models.BigAutoField(primary_key=True,serialize=False)),("title",models.CharField(max_length=200)),("sku",models.CharField(max_length=64,unique=True)),("description",models.TextField(blank=True)),("active",models.BooleanField(default=False)),("created_at",models.DateTimeField(auto_now_add=True)),("subcategory",models.ForeignKey(to="catalog.subcategory",on_delete=deletion.PROTECT,related_name="products"))],options={"ordering":["-created_at"]}),
        migrations.CreateModel(name="ProductMedia", fields=[("id",models.BigAutoField(primary_key=True,serialize=False)),("file",models.FileField(upload_to="products/%Y/%m/")),("kind",models.CharField(max_length=10,choices=[("image","תמונה / GIF"),("video","וידאו")],default="image")),("alt_text",models.CharField(max_length=250,blank=True)),("order",models.PositiveIntegerField(default=0)),("product",models.ForeignKey(to="catalog.product",on_delete=deletion.CASCADE,related_name="media"))],options={"ordering":["order","pk"]}),
        migrations.CreateModel(name="ProductVariant", fields=[("id",models.BigAutoField(primary_key=True,serialize=False)),("width_cm",models.DecimalField(max_digits=6,decimal_places=1)),("height_cm",models.DecimalField(max_digits=6,decimal_places=1)),("price_ils",models.DecimalField(max_digits=9,decimal_places=2)),("stock",models.PositiveIntegerField(default=0)),("product",models.ForeignKey(to="catalog.product",on_delete=deletion.CASCADE,related_name="variants"))]),
        migrations.AddConstraint(model_name="subcategory",constraint=models.UniqueConstraint(fields=["category","slug"],name="unique_subcategory_slug")),
        migrations.AddConstraint(model_name="productvariant",constraint=models.UniqueConstraint(fields=["product","width_cm","height_cm"],name="unique_product_dimensions")),
    ]
