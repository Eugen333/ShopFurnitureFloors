from django.contrib import admin
from .models import Furniture, Flooring


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'dimensions', 'price', 'display_initial_stock', 'display_current_stock')

    # Другие настройки админки для Furniture

    def display_initial_stock(self, obj):
        return obj.initial_stock

    display_initial_stock.short_description = 'Initial Stock'

    def display_current_stock(self, obj):
        return obj.current_stock

    display_current_stock.short_description = 'Current Stock'


@admin.register(Flooring)
class FlooringAdmin(admin.ModelAdmin):
    list_display = ('name', 'dimensions', 'price', 'display_initial_stock', 'display_current_stock')

    # Другие настройки админки для Flooring

    def display_initial_stock(self, obj):
        return obj.initial_stock

    display_initial_stock.short_description = 'Initial Stock'

    def display_current_stock(self, obj):
        return obj.current_stock

    display_current_stock.short_description = 'Current Stock'
