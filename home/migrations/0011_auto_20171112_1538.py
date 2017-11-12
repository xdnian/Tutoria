# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20171112_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='school',
            field=models.CharField(choices=[('1', 'University of Hong Kong'), ('2', 'Hong Kong University of Science and Technology'), ('3', 'Chinese University of Hong Kong'), ('4', 'City University of Hong Kong'), ('5', 'The Hong Kong Polytechnic University'), ('6', 'Hong Kong Baptist University')], default='1', max_length=2),
        ),
    ]