# Generated by Django 3.2.5 on 2021-07-22 20:42

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210721_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amazon_asin',
            field=models.CharField(default=None, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='amazon_url',
            field=models.URLField(default=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='ebay_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='ebay_url',
            field=models.URLField(default=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumb',
            field=cloudinary.models.CloudinaryField(blank=True, default=None, max_length=255, null=True, verbose_name='thumb'),
        ),
    ]
