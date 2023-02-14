# Generated by Django 4.1.4 on 2023-02-14 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MachineAction",
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
                ("camera", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "photo_start",
                    models.CharField(blank=True, max_length=250, null=True),
                ),
                ("photo_stop", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "start_tracking",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "stop_tracking",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
            ],
            options={
                "verbose_name": "MachineAction",
                "verbose_name_plural": "MachineActions",
            },
        ),
    ]
