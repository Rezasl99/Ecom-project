# Generated by Django 5.1 on 2024-11-05 14:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_productview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productview',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
