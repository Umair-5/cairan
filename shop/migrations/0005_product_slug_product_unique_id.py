# Generated by Django 5.1.1 on 2024-09-12 13:11

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='product',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
