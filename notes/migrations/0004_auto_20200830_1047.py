# Generated by Django 3.1 on 2020-08-30 05:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20200830_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phoneno',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^0?[5-9]{1}\\d{9}$')]),
        ),
    ]
