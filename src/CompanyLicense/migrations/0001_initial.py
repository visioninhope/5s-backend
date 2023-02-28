# Generated by Django 4.1.4 on 2023-02-28 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="License",
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
                ("license_key", models.TextField(verbose_name="Company license key")),
                ("name_company", models.TextField(verbose_name="Name of company")),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date joined"),
                ),
                (
                    "date_edited",
                    models.DateTimeField(auto_now=True, verbose_name="Date edited"),
                ),
                (
                    "valid_until",
                    models.DateField(verbose_name="Date which license is active"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="Is active license"
                    ),
                ),
                (
                    "count_cameras",
                    models.IntegerField(verbose_name="Count of cameras in active"),
                ),
                (
                    "neurons_active",
                    models.TextField(verbose_name="List of active neurons"),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Super_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "License",
                "verbose_name_plural": "Licenses",
            },
        ),
    ]
