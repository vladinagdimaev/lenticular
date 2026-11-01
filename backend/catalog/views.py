from django.http import JsonResponse
from .models import Product

def catalog_json(request):
    products = Product.objects.filter(active=True).select_related("subcategory__category").prefetch_related("variants", "media")
    data = []
    for p in products:
        variants = [{"id": v.id, "width_cm": str(v.width_cm), "height_cm": str(v.height_cm),
                     "price_ils": str(v.price_ils), "stock": v.stock} for v in p.variants.all() if v.stock > 0]
        if not variants:
            continue
        data.append({"id": p.id, "sku": p.sku, "title": p.title, "description": p.description,
                     "category": p.subcategory.category.slug, "subcategory": p.subcategory.slug,
                     "variants": variants,
                     "media": [{"url": request.build_absolute_uri(m.file.url), "kind": m.kind, "alt": m.alt_text}
                               for m in p.media.all() if m.file]})
    response = JsonResponse({"products": data})
    response["Access-Control-Allow-Origin"] = request.headers.get("Origin", "") if request.headers.get("Origin", "") in [
        x.strip() for x in __import__("os").environ.get("CATALOG_ALLOWED_ORIGINS", "").split(",") if x.strip()] else ""
    return response
