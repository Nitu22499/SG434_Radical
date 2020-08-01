# Generated by Django 3.0.8 on 2020-08-01 04:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.School'),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
