# Generated by Django 4.1.4 on 2023-04-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DatabaseConnection",
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
                ("database_type", models.CharField(default="OrderView", max_length=50)),
                ("server", models.CharField(max_length=200)),
                ("database", models.CharField(max_length=200)),
                ("username", models.CharField(max_length=200)),
                ("password", models.BinaryField()),
                ("port", models.IntegerField()),
            ],
        ),
    ]
