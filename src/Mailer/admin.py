from django.contrib import admin
from src.Mailer.models import Emails, SMTPSettings


@admin.register(Emails)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("email", "id",)


@admin.register(SMTPSettings)
class SMTPSettingsAdmin(admin.ModelAdmin):
    list_display = ("server", "port", "username", "password", "email_use_tls", "email_use_ssl", "id")
