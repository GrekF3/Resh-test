from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

class Discount(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.amount}% Discount"

class Tax(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.amount}% Tax"

class Order(models.Model):
    items = models.ManyToManyField('Item')
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"Order {self.id}"

    def get_items_display(self):
        return ", ".join([str(item) for item in self.items.all()])

    def calculate_total_amount(self):
        items_total = sum(item.price for item in self.items.all())
        discount = self.discount_set.first()
        tax = self.tax_set.first()

        if discount:
            items_total -= items_total * (discount.amount / 100)

        if tax:
            items_total += items_total * (tax.amount / 100)

        return items_total

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'