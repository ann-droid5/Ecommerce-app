from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category

# List all products (with filters + search)
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # --- Search ---
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(name__icontains=query)
        )

    # --- Category Filter ---
    category_id = request.GET.get("category")
    if category_id and category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    # --- Price Filter ---
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    if price_min and price_min.isdigit():
        products = products.filter(price__gte=int(price_min))
    if price_max and price_max.isdigit():
        products = products.filter(price__lte=int(price_max))

    # --- Availability Filter ---
    in_stock = request.GET.get("in_stock")
    if in_stock == "1":  # only show available products
        products = products.filter(qty_in_stock__gt=0)

    # --- Sorting ---
    sort_by = request.GET.get("sort")
    if sort_by == "price_low":
        products = products.order_by("price")
    elif sort_by == "price_high":
        products = products.order_by("-price")
    elif sort_by == "newest":
        products = products.order_by("-id")  # latest first

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": category_id,
        "price_min": price_min,
        "price_max": price_max,
        "in_stock": in_stock,
        "sort_by": sort_by,
    })


# Show single product detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})


