# Generated by Django 3.1.7 on 2021-08-06 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_bleach.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=100, unique=True, verbose_name='Category')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('functionality', models.CharField(choices=[('Kitchen', 'Kitchen'), ('Bathroom', 'Bathroom'), ('Bedroom', 'Bedroom'), ('Garage', 'Garage'), ('Workspace', 'Workspace'), ('Utilities', 'Utilities')], max_length=20, verbose_name='Predominant functionality')),
                ('description', django_bleach.models.BleachField()),
                ('builder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_identification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_base', models.CharField(max_length=100, verbose_name='Project Base')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Name')),
                ('vehicle_description', django_bleach.models.BleachField()),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('build_techniques', models.CharField(choices=[('aluminum extrusions', 'aluminum extrusions'), ('welding', 'welding'), ('carpentry', 'carpentry'), ('fiberglass', 'fiberglass'), ('CNC', 'CNC'), ('foam', 'foam')], max_length=20, verbose_name='Predominant build technique')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle_pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='uploads/vehicle_pictures')),
                ('annotation', models.TextField(blank=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='website.vehicle_identification')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('tree_linked', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='website.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', django_bleach.models.BleachField()),
                ('location', models.CharField(blank=True, max_length=30, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='static/profile_pic_default.png', null=True, upload_to='uploads/profile_pic')),
                ('website', models.URLField(blank=True, default=None, max_length=100, null=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('subject', models.CharField(max_length=80)),
                ('message', django_bleach.models.BleachField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Furniture_pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='uploads/furniture_pictures')),
                ('annotation', models.TextField(blank=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='website.furniture')),
            ],
        ),
        migrations.CreateModel(
            name='Furniture_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='website.furniture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Furniture_comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=80, null=True)),
                ('message', models.TextField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.furniture')),
            ],
        ),
        migrations.AddField(
            model_name='furniture',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='furnitures', to='website.vehicle_identification'),
        ),
    ]
