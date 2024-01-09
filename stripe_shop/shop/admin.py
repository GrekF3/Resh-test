from django.contrib import admin
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description']

class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1

class TaxInline(admin.TabularInline):
    model = Tax
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_items_display', 'get_tax_display', 'get_discount_display', 'total_amount')

    inlines = [
        TaxInline,
        DiscountInline,
    ]

    def get_items_display(self, obj):
        return obj.get_items_display()

    def get_tax_display(self, obj):
        tax = obj.tax_set.first()
        return tax.amount if tax else None

    def get_discount_display(self, obj):
        discount = obj.discount_set.first()
        return discount.amount if discount else None

    def total_amount(self, obj):
        return obj.calculate_total_amount()

    get_items_display.short_description = 'Items'
    get_tax_display.short_description = 'Tax'
    get_discount_display.short_description = 'Discount'
    total_amount.short_description = 'Total Amount'

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    pass
