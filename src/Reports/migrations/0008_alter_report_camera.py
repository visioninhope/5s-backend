# Generated by Django 4.1.4 on 2023-05-13 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cameras", "0004_alter_camera_table"),
        ("Reports", "0007_rename_zlecenia_index_skanyreport_zlecenie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="camera",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Cameras.camera",
            ),
        ),
    ]
