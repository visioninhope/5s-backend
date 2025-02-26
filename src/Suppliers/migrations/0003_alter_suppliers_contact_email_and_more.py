# Generated by Django 4.2.1 on 2023-06-08 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Suppliers", "0002_suppliers_country_suppliers_first_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="suppliers",
            name="contact_email",
            field=models.EmailField(
                default=None, max_length=254, verbose_name="Contact email suppliers"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="suppliers",
            name="website",
            field=models.TextField(
                blank=True, null=True, verbose_name="Website of suppliers"
            ),
        ),
    ]
