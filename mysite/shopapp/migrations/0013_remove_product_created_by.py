# Generated by Django 4.2.4 on 2023-11-15 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0012_alter_product_description_alter_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
    ]
