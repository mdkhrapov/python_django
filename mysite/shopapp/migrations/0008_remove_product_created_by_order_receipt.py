# Generated by Django 4.2.4 on 2023-10-17 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_product_options_product_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='orders/receipts/'),
        ),
    ]
