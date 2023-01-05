# Generated by Django 4.1.4 on 2023-01-05 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default='Unknown', max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, default='Unknown', max_length=40, null=True)),
                ('dataset', models.TextField(blank=True, null=True, verbose_name='Date Set user')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='')),
                ('status', models.BooleanField(default=False, verbose_name='Status in location')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employers',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('release_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Location_users', to='Locations.location')),
                ('people', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='people_in_location', to='Employees.customuser')),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'Stories',
            },
        ),
    ]
