# Generated by Django 5.0.1 on 2024-01-05 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_item_options_order_discount_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
    ]
