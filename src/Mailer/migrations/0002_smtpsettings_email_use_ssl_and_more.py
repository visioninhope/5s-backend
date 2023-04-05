# Generated by Django 4.1.4 on 2023-04-04 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Mailer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="smtpsettings",
            name="email_use_ssl",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="smtpsettings",
            name="email_use_tls",
            field=models.BooleanField(default=False),
        ),
    ]
