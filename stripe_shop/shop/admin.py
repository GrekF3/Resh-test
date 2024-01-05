from django.contrib import admin
from .models import Item, Order, Discount, Tax
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_items_display')

    def get_items_display(self, obj):
        return obj.get_items_display()

    get_items_display.short_description = 'Items'
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    pass
