from django.core.files import File
import os

from django.core.management.base import BaseCommand
from Statistics.models import *

import urllib
from urllib import request
from urllib.request import urlretrieve
import json


class Command(BaseCommand):
	args = 'not required'
	help = 'populates or verifies/updates fixture data for all gameweek objects'

	def populate_fixture_objects(self):
		api_token = 'VLOpn8fyodXRigQlOuxzzgfI1D2IW6risWDraB3u4jYPCTUlwTH4EOcV8a6o'
		gameweeks = Gameweek.objects.all()

		for g in gameweeks:
			url = 'https://soccer.sportmonks.com/api/v2.0/rounds/'+str(g.gw_id)+'?api_token='+api_token+'&include=fixtures'
			d = json.load(urllib.request.urlopen(url))
			a = d['data']
			b = a['fixtures']
			c = b['data']
			y = len(c)
			for i in range(0,y):
				x = c[i]
				n = x['id']
				if Fixture.objects.filter(fixture_id = n).exists():
					f = Fixture.objects.get(fixture_id = n)
					f.fixture_id= x['id']
					fixture_gameweek = g
					v = x['venue_id']
					f.fixture_venue = Venue.objects.get(venue_id = v)
					t = x['time']
					t_s = t['starting_at']
					f.fixture_start = t_s['date_time']
					th = x['localteam_id'] 
					f.fixture_team_home = Team.objects.get(team_id = th)
					ta = x['visitorteam_id']
					f.fixture_team_away = Team.objects.get(team_id = ta)
					xs = x['scores']
					f.fixture_ht_score = xs['ht_score']
					f.fixture_ft_score = xs['ft_score']
					f.save()
				else:
					v = x['venue_id']
					if Venue.objects.filter(venue_id = v).exists():
						v_obj = Venue.objects.get(venue_id = v)
					else:
						url_two = 'https://soccer.sportmonks.com/api/v2.0/venues/'+str(x['venue_id'])+'?api_token='+api_token
						d_two = json.load(urllib.request.urlopen(url_two))
						y = d_two['data']
						v = Venue(venue_id = y['id'], venue_name = y['name'], venue_city = y['city'], venue_capacity = y['capacity'])
						v.save()
						v_obj = Venue.objects.get(venue_id = v)

					th = x['localteam_id'] 
					th_obj = Team.objects.get(team_id = th)
					ta = x['visitorteam_id'] 
					ta_obj = Team.objects.get(team_id = ta)
					xs = x['scores']
					t = x['time']
					t_s = t['starting_at']
					f_s = t_s['date_time']
					f = Fixture(fixture_id = x['id'], fixture_gameweek = g, fixture_venue = v_obj, fixture_start = f_s, fixture_team_home = th_obj, fixture_team_away = ta_obj, fixture_ht_score = xs['ht_score'], fixture_ft_score = xs['ft_score'])
					f.save()

		print('Data Collection Done')

	def handle(self, *args, **options):
		self.populate_fixture_objects()		