# Generated by Django 4.1.4 on 2023-05-16 06:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Reports", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="report",
            table="report",
        ),
        migrations.AlterModelTable(
            name="skanyreport",
            table="skany_report",
        ),
    ]
