# Generated by Django 5.1.1 on 2024-09-20 17:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_product_status_delete_cart"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="description",
            new_name="Address",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="price",
            new_name="Fees",
        ),
        migrations.AddField(
            model_name="product",
            name="end_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="product",
            name="start_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
