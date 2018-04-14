# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 12:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Statistics', '0007_fixture_fixture_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture_Team_Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fts_team_type', models.CharField(choices=[('Home', 'Home'), ('Away', 'Away')], max_length=5)),
                ('fts_formation', models.CharField(max_length=10)),
                ('fts_score', models.IntegerField()),
                ('fts_corners', models.IntegerField()),
                ('fts_fouls_committed', models.IntegerField()),
                ('fts_fouls_drawn', models.IntegerField()),
                ('fts_goalkicks', models.IntegerField()),
                ('fts_offsides', models.IntegerField()),
                ('fts_passes_total', models.IntegerField()),
                ('fts_passes_accuracy', models.IntegerField()),
                ('fts_possession', models.IntegerField()),
                ('fts_yellowcards', models.IntegerField()),
                ('fts_redcards', models.IntegerField()),
                ('fts_saves', models.IntegerField()),
                ('fts_shots_total', models.IntegerField()),
                ('fts_shots_ontarget', models.IntegerField()),
                ('fts_shots_offtarget', models.IntegerField()),
                ('fts_shots_blocked', models.IntegerField()),
                ('fts_shots_insidebox', models.IntegerField()),
                ('fts_shots_outsidebox', models.IntegerField()),
                ('fts_substitutions', models.IntegerField()),
                ('fts_fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fixture_Team_Stats', to='Statistics.Fixture')),
                ('fts_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Team_Details', to='Statistics.Team')),
            ],
        ),
    ]
