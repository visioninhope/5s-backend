# Generated by Django 4.1.4 on 2023-05-16 07:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.CharField(max_length=250)),
                ("date", models.CharField(max_length=250)),
            ],
            options={
                "verbose_name": "ImageReport",
                "verbose_name_plural": "ImageReports",
            },
        ),
    ]
