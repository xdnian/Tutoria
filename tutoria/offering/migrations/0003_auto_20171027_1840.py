# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 10:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offering', '0002_timeslot_tutor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='slots',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
