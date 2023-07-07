# Generated by Django 4.2.1 on 2023-07-07 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Inventory", "0007_items_object_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="items",
            name="object_type",
            field=models.CharField(
                choices=[("bottles", "Bottles"), ("boxes", "Boxes")],
                default="boxes",
                max_length=20,
                verbose_name="Object type",
            ),
        ),
    ]
