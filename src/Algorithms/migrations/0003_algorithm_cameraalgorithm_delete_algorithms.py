# Generated by Django 4.1.4 on 2023-02-13 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Locations", "0002_camera_password_camera_username"),
        ("Algorithms", "0002_rename_is_active_algorithms_is_available_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Algorithm",
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
                ("name", models.CharField(max_length=100)),
                ("is_available", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="CameraAlgorithm",
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
                    "algorithm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Algorithms.algorithm",
                    ),
                ),
                (
                    "camera_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Locations.camera",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Algorithms",
        ),
    ]
