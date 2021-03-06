# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 08:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Statistics', '0020_auto_20171011_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.IntegerField(null=True)),
                ('card_type', models.CharField(max_length=10)),
                ('card_time', models.IntegerField(null=True)),
                ('card_fixture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Card_Fixture', to='Statistics.Fixture')),
                ('card_player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Card', to='Statistics.Player')),
                ('card_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Card_Team', to='Statistics.Team')),
            ],
        ),
    ]
