# Generated by Django 4.2.1 on 2023-06-19 09:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Inventory", "0004_alter_items_suppliers"),
    ]

    operations = [
        migrations.AddField(
            model_name="items",
            name="copy_emails",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.EmailField(max_length=254),
                blank=True,
                null=True,
                size=None,
                verbose_name="Emails",
            ),
        ),
        migrations.AddField(
            model_name="items",
            name="subject",
            field=models.CharField(
                blank=True, max_length=60, null=True, verbose_name="Subject message"
            ),
        ),
        migrations.AddField(
            model_name="items",
            name="to_emails",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.EmailField(max_length=254),
                blank=True,
                null=True,
                size=None,
                verbose_name="Emails",
            ),
        ),
    ]
