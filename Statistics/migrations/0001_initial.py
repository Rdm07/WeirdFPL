# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 05:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gameweek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gw_id', models.IntegerField()),
                ('gw_number', models.IntegerField()),
                ('gw_start', models.DateField()),
                ('gw_end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_id', models.IntegerField()),
                ('season_name', models.CharField(max_length=10)),
                ('is_current', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='gameweek',
            name='gw_season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Statistics.Season'),
        ),
    ]
