# Generated by Django 5.1 on 2024-08-15 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_otpcode_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
