# Generated by Django 4.1.4 on 2023-02-20 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Reports", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                ("image", models.CharField(max_length=250)),
                ("date", models.CharField(max_length=250)),
                (
                    "report_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="Reports.report",
                    ),
                ),
            ],
            options={
                "verbose_name": "ImageReport",
                "verbose_name_plural": "ImageReports",
            },
        ),
    ]
