# Generated by Django 5.0.4 on 2024-04-28 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poseapp', '0007_apikey_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('firebase_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='apikey',
            name='gender',
        ),
        migrations.AlterField(
            model_name='apikey',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='poseapp.user'),
        ),
    ]
