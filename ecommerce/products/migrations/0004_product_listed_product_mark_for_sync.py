# Generated by Django 5.0.1 on 2024-01-24 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_options_remove_category_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='listed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='mark_for_sync',
            field=models.BooleanField(default=False),
        ),
    ]
