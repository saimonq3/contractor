# Generated by Django 5.1.4 on 2025-02-17 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dto', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmembers',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='members',
            name='created_by',
        ),
    ]
