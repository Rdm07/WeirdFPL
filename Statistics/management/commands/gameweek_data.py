from django.core.management.base import BaseCommand
from Statistics.models import *

import urllib
from urllib import request
import json


class Command(BaseCommand):
	args = 'not required'
	help = 'populates or verifies/updates gameweek data for all season objects'

	def populate_gameweek_objects(self):
		api_token = 'VLOpn8fyodXRigQlOuxzzgfI1D2IW6risWDraB3u4jYPCTUlwTH4EOcV8a6o'
		seasons = Season.objects.all()

		for s in seasons:
			url = 'https://soccer.sportmonks.com/api/v2.0/seasons/'+str(s.season_id)+'?api_token='+api_token+'&include=rounds'
			d = json.load(urllib.request.urlopen(url))
			a = d['data']
			b = a['rounds']
			c = b['data']
			y = len(c)
			for i in range(0,y):
				x = c[i]
				if Gameweek.objects.filter(gw_number = i+1, gw_season = s).exists():
					g = Gameweek.objects.get(gw_number = i+1, gw_season = s)
					g.gw_id = x['id']
					g.gw_number = x['name']
					g.gw_start = x['start']
					g.gw_end = x['end']
					g.save()
				else:
					g = Gameweek(gw_id = x['id'], gw_number = x['name'], gw_start = x['start'], gw_end = x['end'], gw_season = s)
					g.save()

		print('Data Collection Done')

	def handle(self, *args, **options):
		self.populate_gameweek_objects()