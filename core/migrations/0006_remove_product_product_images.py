# Generated by Django 5.0.6 on 2024-06-19 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_product_created_at_remove_product_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_images',
        ),
    ]
