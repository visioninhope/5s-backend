# Generated by Django 4.2.1 on 2023-07-18 09:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DatabaseConnections", "0002_databaseconnection_dbms"),
    ]

    operations = [
        migrations.AddField(
            model_name="databaseconnection",
            name="is_active",
            field=models.BooleanField(default=True, unique=True),
        ),
        migrations.AlterField(
            model_name="databaseconnection",
            name="dbms",
            field=models.CharField(
                choices=[("postgres", "PostgreSQL"), ("mssql", "Microsoft SQL Server")],
                default="mssql",
                max_length=50,
            ),
        ),
    ]
