from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  

class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order, OrdersAdmin)
