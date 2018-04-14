# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Statistics', '0003_remove_team_team_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_id', models.IntegerField()),
                ('venue_name', models.CharField(max_length=50)),
                ('venue_city', models.CharField(max_length=50)),
                ('venue_capacity', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='team_venue',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Statistics.Venue'),
            preserve_default=False,
        ),
    ]
