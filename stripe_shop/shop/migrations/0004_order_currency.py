# Generated by Django 5.0.1 on 2024-01-05 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_item_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='currency',
            field=models.CharField(default='USD', max_length=3),
        ),
    ]
