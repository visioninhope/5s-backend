from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    date_set = models.TextField(verbose_name='Date Set user', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'


