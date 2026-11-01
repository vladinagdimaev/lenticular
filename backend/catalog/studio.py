from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import slugify
from .models import Category, Subcategory, Product, ProductMedia, ProductVariant
import os
import uuid

@staff_member_required(login_url="/admin/login/")
def studio(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "upload":
            files = request.FILES.getlist("files")
            sub = Subcategory.objects.filter(pk=request.POST.get("subcategory")).first()
            if not sub:
                messages.error(request, "יש לבחור תת־קטגוריה")
            elif not files:
                messages.error(request, "לא נבחרו קבצים")
            else:
                count = 0
                for file in files:
                    kind = "video" if file.content_type.startswith("video/") else "image" if file.content_type.startswith("image/") else None
                    if not kind:
                        continue
                    title = os.path.splitext(file.name)[0][:200]
                    with transaction.atomic():
                        p = Product.objects.create(title=title, sku="B-" + uuid.uuid4().hex[:12].upper(), subcategory=sub, active=False)
                        ProductMedia.objects.create(product=p, file=file, kind=kind, alt_text=title)
                        ProductVariant.objects.create(product=p, width_cm=30, height_cm=40, price_ils=40, stock=1)
                    count += 1
                messages.success(request, f"נוצרו {count} מוצרים כטיוטות. אפשר לערוך ולפרסם אותם למטה.")
        elif action == "delete":
            product = Product.objects.filter(pk=request.POST.get("product_id")).first()
            if product:
                name = product.title
                product.delete()
                messages.success(request, f"המוצר {name} נמחק מהקטלוג")
            else:
                messages.error(request, "המוצר לא נמצא")
        elif action == "save":
            ids = request.POST.getlist("ids")
            count = 0
            for value in ids:
                p = Product.objects.filter(pk=value).first()
                if not p:
                    continue
                title = request.POST.get(f"title_{value}", "").strip()
                sub = Subcategory.objects.filter(pk=request.POST.get(f"subcategory_{value}")).first()
                if not title or not sub:
                    continue
                p.title = title[:200]
                p.subcategory = sub
                p.active = request.POST.get(f"active_{value}") == "on"
                p.save(update_fields=["title", "subcategory", "active"])
                v = p.variants.first()
                if v:
                    try:
                        width = float(request.POST.get(f"width_{value}", 30))
                        height = float(request.POST.get(f"height_{value}", 40))
                        stock = int(request.POST.get(f"stock_{value}", 0))
                        if width > 0 and height > 0 and stock >= 0:
                            v.width_cm, v.height_cm, v.stock = width, height, stock
                            v.save(update_fields=["width_cm", "height_cm", "stock"])
                    except (ValueError, TypeError):
                        pass
                count += 1
            messages.success(request, f"נשמרו {count} מוצרים")
        return redirect("studio")
    return render(request, "catalog/studio.html", {
        "products": Product.objects.select_related("subcategory").prefetch_related("media", "variants").order_by("-created_at")[:200],
        "subcategories": Subcategory.objects.select_related("category").all(),
    })
