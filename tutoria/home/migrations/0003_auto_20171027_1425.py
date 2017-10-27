# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_profile_birth_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='location',
            new_name='school',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.AddField(
            model_name='profile',
            name='identity',
            field=models.CharField(choices=[('S', 'Stuent'), ('T', 'Tutor')], default='S', max_length=2),
        ),
    ]
