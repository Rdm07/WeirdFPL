# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-10 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Statistics', '0015_auto_20171010_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='goal_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='substitution',
            name='sub_time',
            field=models.IntegerField(null=True),
        ),
    ]
