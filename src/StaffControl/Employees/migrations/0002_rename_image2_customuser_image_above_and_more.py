# Generated by Django 4.1.4 on 2023-02-15 11:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Employees", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="image2",
            new_name="image_above",
        ),
        migrations.RenameField(
            model_name="customuser",
            old_name="image1",
            new_name="image_below",
        ),
        migrations.RenameField(
            model_name="customuser",
            old_name="image3",
            new_name="image_center",
        ),
        migrations.RenameField(
            model_name="customuser",
            old_name="image4",
            new_name="image_left",
        ),
        migrations.RenameField(
            model_name="customuser",
            old_name="image5",
            new_name="image_right",
        ),
    ]
