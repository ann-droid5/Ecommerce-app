from django.contrib import admin

from django.contrib import admin
from .models import Category, Product, Order, OrderDetail, Cart, Log

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Cart)
admin.site.register(Log)

