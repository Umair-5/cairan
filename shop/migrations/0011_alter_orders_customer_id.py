# Generated by Django 5.1.1 on 2024-11-08 21:39

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_orders_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='customer_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
