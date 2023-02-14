# Generated by Django 4.1.4 on 2023-02-14 14:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("IdleControl", "0002_alter_actions_options_alter_photos_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="actions",
            name="start_tracking",
            field=models.DateTimeField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="actions",
            name="stop_tracking",
            field=models.DateTimeField(blank=True, max_length=50, null=True),
        ),
    ]
