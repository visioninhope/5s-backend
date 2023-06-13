# Generated by Django 4.2.1 on 2023-06-09 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("CompanyLicense", "0005_company_my_company"),
        ("Inventory", "0003_items_order_quantity_items_suppliers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="items",
            name="suppliers",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="Supplier",
                to="CompanyLicense.company",
            ),
        ),
    ]
