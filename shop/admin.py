# ShopFurnitureFloors\shop\admin.py

from django.contrib import admin
from .models import Furniture, Flooring
from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)


class StockAdminMixin:
    list_display = ('id', 'name', 'dimensions', 'price', 'initial_stock', 'current_stock', 'product_type')

    def initial_stock(self, obj):
        return obj.initial_stock if hasattr(obj, 'initial_stock') else None

    initial_stock.short_description = 'Initial Stock'

    def current_stock(self, obj):
        return obj.current_stock if hasattr(obj, 'current_stock') else None

    current_stock.short_description = 'Current Stock'


@admin.register(Furniture)
class FurnitureAdmin(StockAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Flooring)
class FlooringAdmin(StockAdminMixin, admin.ModelAdmin):
    pass
