# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20171027_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]