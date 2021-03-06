# Generated by Django 3.1.7 on 2021-08-11 22:34

from django.db import migrations, models
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_project_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle_identification',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle_identification',
            name='vehicle_description',
            field=django_bleach.models.BleachField(),
        ),
    ]
