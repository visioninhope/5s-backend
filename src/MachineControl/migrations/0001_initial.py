# Generated by Django 4.1.4 on 2023-02-15 06:23

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
                ("camera", models.CharField(default="now ip", max_length=50)),
                ("photo_start", models.CharField(default="now photo", max_length=250)),
                ("photo_stop", models.CharField(default="now photo", max_length=250)),
                ("start_tracking", models.TextField(default=None, max_length=150)),
                ("stop_tracking", models.TextField(default=None, max_length=150)),
            ],
            options={
                "verbose_name": "MachineAction",
                "verbose_name_plural": "MachineActions",
            },
        ),
    ]
