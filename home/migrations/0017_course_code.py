# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20171119_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
