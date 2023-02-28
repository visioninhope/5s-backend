# Generated by Django 4.1.4 on 2023-02-28 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Cameras", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gate",
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
                ("name", models.CharField(max_length=30)),
                (
                    "camera_input",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="DeviceInput",
                        to="Cameras.camera",
                    ),
                ),
                (
                    "camera_output",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="DeviceOutput",
                        to="Cameras.camera",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=30)),
                (
                    "gate_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Gate",
                        to="Locations.gate",
                    ),
                ),
            ],
            options={
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
            },
        ),
    ]
