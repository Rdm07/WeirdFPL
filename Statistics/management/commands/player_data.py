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
	help = 'populates or verifies/updates player data for all team objects'

	def populate_player_objects(self):
		api_token = 'VLOpn8fyodXRigQlOuxzzgfI1D2IW6risWDraB3u4jYPCTUlwTH4EOcV8a6o'
		teams = Team.objects.all()

		for t in teams:
			url = 'https://soccer.sportmonks.com/api/v2.0/teams/'+str(t.team_id)+'?api_token='+api_token+'&include=squad'
			d = json.load(urllib.request.urlopen(url))
			a = d['data']
			b = a['squad']
			c = b['data']
			y = len(c)
			player_ids = []
			for i in range(0,y):
				x = c[i]
				n = x['player_id']
				urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(n)+'?api_token='+api_token
				dtwo = json.load(urllib.request.urlopen(urltwo))
				atwo = dtwo['data']
				if Player.objects.filter(player_id = n).exists():
					p = Player.objects.get(player_id = n)
					p.player_id = n
					p.player_team = t
					p.player_name = atwo['fullname']
					p.player_common_name = atwo['common_name']
					p.player_nationality = atwo['nationality']
					p.player_height = atwo['height']
					p.player_weight = atwo['weight']
					p.save()
				else:
					p = Player(player_id = n)
					p.player_team = t
					p.player_name = atwo['fullname']
					p.player_common_name = atwo['common_name']
					p.player_nationality = atwo['nationality']
					p.player_height = atwo['height']
					p.player_weight = atwo['weight']
					p.save()

		print('Data Collection Done')
				
	def handle(self, *args, **options):
		self.populate_player_objects()		