# Generated by Django 4.1.4 on 2023-05-15 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Emails",
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
                    "email",
                    models.EmailField(
                        max_length=254, verbose_name="Email to send notifications"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is activ email"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SMTPSettings",
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
                ("server", models.CharField(max_length=255)),
                ("port", models.IntegerField()),
                ("username", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("email_use_tls", models.BooleanField(default=False)),
                ("email_use_ssl", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="WorkingTime",
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
                ("time_start", models.TimeField(verbose_name="Start time")),
                ("time_end", models.TimeField(verbose_name="End time")),
            ],
        ),
    ]
