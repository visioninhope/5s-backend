# Generated by Django 4.1.4 on 2023-04-10 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Cameras", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IndexOperations",
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
                (
                    "type_operation",
                    models.IntegerField(verbose_name="id_stanowisko operation control"),
                ),
                (
                    "camera",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Cameras.camera",
                        verbose_name="operations_control camera",
                    ),
                ),
            ],
        ),
    ]
