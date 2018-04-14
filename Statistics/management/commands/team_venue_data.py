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
	help = 'populates or verifies/updates team data for all season objects'

	def populate_team_objects(self):
		api_token = 'VLOpn8fyodXRigQlOuxzzgfI1D2IW6risWDraB3u4jYPCTUlwTH4EOcV8a6o'
		seasons = Season.objects.all()

		for s in seasons:
			url_one = 'https://soccer.sportmonks.com/api/v2.0/teams/season/'+str(s.season_id)+'?api_token='+api_token
			d_one = json.load(urllib.request.urlopen(url_one))
			a = d_one['data']
			n = len(a)
			for i in range(0,n):
				x = a[i]
				url_two = 'https://soccer.sportmonks.com/api/v2.0/venues/'+str(x['venue_id'])+'?api_token='+api_token
				d_two = json.load(urllib.request.urlopen(url_two))
				y = d_two['data']

				v_id = y['id']
				if Venue.objects.filter(venue_id = v_id).exists():
					pass
				else:
					v = Venue(venue_id = y['id'], venue_name = y['name'], venue_city = y['city'], venue_capacity = y['capacity'])
					v.save()

				t_id = x['id']
				if Team.objects.filter(team_id = t_id).exists():
					pass
				else:
					v = Venue.objects.get(venue_name = y['name'])
					t = Team(team_id = x['id'], team_name = x['name'], team_venue = v)
					t.save()

		print('Data Collection Done')

	def handle(self, *args, **options):
		self.populate_team_objects()		