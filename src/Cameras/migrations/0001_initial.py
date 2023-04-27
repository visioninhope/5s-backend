# Generated by Django 4.1.4 on 2023-04-10 11:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Camera",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=30,
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="ID must be a valid IP address",
                                regex="^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$",
                            )
                        ],
                    ),
                ),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=250)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Camera",
                "verbose_name_plural": "Cameras",
            },
        ),
    ]
