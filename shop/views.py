from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem

# Show all categories
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/categories.html', {'categories': categories})

# Show products in a category
def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/products.html', {'category': category, 'products': products})

# Add product to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

# View cart
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'shop/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })

# Remove product from cart
def remove_from_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    return redirect('cart_detail')
