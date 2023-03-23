# Generated by Django 4.1.4 on 2023-03-23 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Cameras", "0002_alter_camera_password_alter_camera_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="Items",
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
                ("name", models.TextField(max_length=75, verbose_name="Item name")),
                ("status", models.CharField(default="Out of stock", max_length=20)),
                (
                    "current_stock_level",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Current stock level"
                    ),
                ),
                (
                    "low_stock_level",
                    models.IntegerField(verbose_name="Low stock level"),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="Email to send notifications",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date created"
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Date updated"),
                ),
                (
                    "coords",
                    models.TextField(
                        blank=True, null=True, verbose_name="Area coordinates"
                    ),
                ),
                (
                    "camera",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="camera_id",
                        to="Cameras.camera",
                    ),
                ),
            ],
        ),
    ]
