# Generated by Django 5.1.3 on 2024-11-08 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]