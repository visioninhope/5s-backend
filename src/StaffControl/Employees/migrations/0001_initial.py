# Generated by Django 4.1.4 on 2023-04-10 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffControlUser",
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
                    "first_name",
                    models.CharField(
                        blank=True, default="Unknown", max_length=40, null=True
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, default="Unknown", max_length=40, null=True
                    ),
                ),
                (
                    "dataset",
                    models.TextField(
                        blank=True, null=True, verbose_name="Date Set user"
                    ),
                ),
                (
                    "image_below",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="photo below"
                    ),
                ),
                (
                    "image_above",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="photo from above",
                    ),
                ),
                (
                    "image_center",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="photo in the center",
                    ),
                ),
                (
                    "image_left",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="photo on the left",
                    ),
                ),
                (
                    "image_right",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="",
                        verbose_name="photo on the right",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        default=False, verbose_name="Status in location"
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="location",
                        to="Locations.location",
                    ),
                ),
            ],
            options={
                "verbose_name": "Employee",
                "verbose_name_plural": "Employers",
            },
        ),
    ]
