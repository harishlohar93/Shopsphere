# Generated by Django 5.1.4 on 2025-01-12 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0002_colorvariant_sizevariant_product_color_variant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color_variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.colorvariant'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size_variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.sizevariant'),
        ),
    ]
