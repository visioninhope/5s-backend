# Generated by Django 4.1.4 on 2023-05-22 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("CameraAlgorithms", "0001_initial"),
        ("Reports", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="camera",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="CameraAlgorithms.camera",
            ),
        ),
    ]
