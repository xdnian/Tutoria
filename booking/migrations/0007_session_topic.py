# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_session_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='topic',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
