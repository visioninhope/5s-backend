# Generated by Django 4.1.4 on 2023-05-04 14:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Cameras", "0002_rename_password_camera__password"),
    ]

    operations = [
        migrations.RenameField(
            model_name="camera",
            old_name="_password",
            new_name="password",
        ),
    ]
