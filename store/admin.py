from django.contrib import admin
from .models import Product, Category, Manufacturer, Supplier, Order, OrderItem, PickupPoint

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'price', 'discount_percent', 'stock_quantity')
    list_filter = ('category', 'manufacturer', 'supplier')
    search_fields = ('article', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_date', 'status')
    list_filter = ('status',)
