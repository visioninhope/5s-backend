# Generated by Django 4.1.4 on 2023-02-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OperationsCounter",
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
                    "date_time",
                    models.CharField(max_length=50, verbose_name="datetime_operations"),
                ),
                ("date_created", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Counter",
                "verbose_name_plural": "Counters",
            },
        ),
    ]
