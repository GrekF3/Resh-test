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

class Order(models.Model):

    items = models.ManyToManyField('Item')
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return f"Order {self.id}"

    def get_items_display(self):
        return ", ".join([str(item) for item in self.items.all()])

class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Tax(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)