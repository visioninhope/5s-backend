# Generated by Django 4.1.4 on 2023-02-14 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("IdleControl", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="actions",
            options={
                "verbose_name": "IdleAction",
                "verbose_name_plural": "IdleActions",
            },
        ),
        migrations.AlterModelOptions(
            name="photos",
            options={
                "verbose_name": "PhotoAction",
                "verbose_name_plural": "PhotoActions",
            },
        ),
        migrations.AlterField(
            model_name="photos",
            name="idle_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="IdleControl.actions",
            ),
        ),
    ]
