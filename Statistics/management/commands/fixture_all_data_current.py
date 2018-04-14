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
	help = 'populates or verifies/updates fixture stats data for all fixture objects currently in progress'

	def populate_fixture_data_objects(self):
		api_token = 'VLOpn8fyodXRigQlOuxzzgfI1D2IW6risWDraB3u4jYPCTUlwTH4EOcV8a6o'
		gameweeks = Gameweek.objects.all()
		gw_current = None

		for g in gameweeks:
			if g.gw_started == True:
				if g.gw_finished == False:
					gw_current = g

		if gw_current is not None:
			fixtures = Fixture.objects.filter(fixture_gameweek = gw_current)

			for f in fixtures:
				if f.fixture_started == True:
					if f.fixture_finished == False:
						fixture_id = f.fixture_id
						url = 'https://soccer.sportmonks.com/api/v2.0/fixtures/'+str(fixture_id)+'?api_token='+api_token+'&include=stats,lineup,bench,goals,substitutions,cards'

			# ---------------------- FIXTURE TEAM STATS ------------------------------------------------------------- #

						if FixtureTeamStat.objects.filter(fts_fixture = f).exists():
							if f.fixture_finished == True:
								print('Fixture '+str(f.fixture_id)+' skipped for Fixture Team Statistics')
								pass
							else:
								print('Fixture '+str(f.fixture_id)+' - data edited for Fixture Player Statistics')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['stats']
								c = b['data']
								y = len(c)
								fts_list = FixtureTeamStat.objects.filter(fts_fixture = f)
								for fts in fts_list:
									for i in range(0,y):
										x = c[i]
										team_id = x['team_id']
										if fts.fts_team.team_id == team_id:
											fts.fts_corners = x['corners']
											fts.fts_fouls_committed = x['fouls']
											fts.fts_fouls_drawn = x['free_kick']
											fts.fts_goalkicks = x['goal_kick']
											fts.fts_offsides = x['offsides']
											j = x['passes']
											fts.fts_passes_total = j['total']
											fts.fts_passes_accuracy = j['percentage']
											fts.fts_possession = x['possessiontime']
											fts.fts_yellowcards = x['yellowcards']
											fts.fts_redcards = x['redcards']
											fts.fts_saves = x['saves']
											k = x['shots']
											fts.fts_shots_total = k['total']
											fts.fts_shots_ontarget = k['ongoal']
											fts.fts_shots_offtarget = k['offgoal']
											fts.fts_shots_blocked = k['blocked']
											fts.fts_shots_insidebox = k['insidebox']
											fts.fts_shots_outsidebox = k['outsidebox']
											fts.fts_substitutions = x['substitutions']
											fts.save()
						else:
							if f.fixture_started == True:
								print('Fixture '+str(f.fixture_id)+' - data added for Fixture Team Statistics for the first time')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['stats']
								c = b['data']
								y = len(c)
								local_team_id = a['localteam_id']
								visitor_team_id = a['visitorteam_id']
								# local_team = Team.objects.get(team_id = local_team_id)
								# visitor_team = Team.objects.get(team_id = visitor_team_id)

								for i in range(0,y):
									x = c[i]
									fts = FixtureTeamStat(fts_fixture = f)
									team_id = x['team_id']
									fts.fts_team = Team.objects.get(team_id = team_id)
									e = a['formations']
									h = a['scores']
									if team_id == local_team_id:
										fts.fts_team_type = 'Home'
										fts.fts_formation = e['localteam_formation']
										fts.fts_score = h['localteam_score']
									elif team_id == visitor_team_id:
										fts.fts_team_type = 'Away'
										fts.fts_formation = e['visitorteam_formation']
										fts.fts_score = h['visitorteam_score']
									fts.fts_corners = x['corners']
									fts.fts_fouls_committed = x['fouls']
									fts.fts_fouls_drawn = x['free_kick']
									fts.fts_goalkicks = x['goal_kick']
									fts.fts_offsides = x['offsides']
									j = x['passes']
									fts.fts_passes_total = j['total']
									fts.fts_passes_accuracy = j['percentage']
									fts.fts_possession = x['possessiontime']
									fts.fts_yellowcards = x['yellowcards']
									fts.fts_redcards = x['redcards']
									fts.fts_saves = x['saves']
									k = x['shots']
									fts.fts_shots_total = k['total']
									fts.fts_shots_ontarget = k['ongoal']
									fts.fts_shots_offtarget = k['offgoal']
									fts.fts_shots_blocked = k['blocked']
									fts.fts_shots_insidebox = k['insidebox']
									fts.fts_shots_outsidebox = k['outsidebox']
									fts.fts_substitutions = x['substitutions']
									fts.save()

			# ---------------------- FIXTURE PLAYER STATS ------------------------------------------------------------- #
					
						if FixturePlayerStat.objects.filter(fps_fixture = f).exists():
							if f.fixture_finished == True:
								print('Fixture '+str(f.fixture_id)+' skipped for Fixture Player Statistics')
								pass
							else:
								print('Fixture '+str(f.fixture_id)+' - data edited for Fixture Player Statistics')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['lineup']
								c = b['data']
								b = a['bench']
								e = b['data']
								y = len(e)
								for i in range(0,y):
									c.append(e[i])

								y = len(c)

								fps_list = FixturePlayerStat.objects.filter(fps_fixture = f)
								for fps in fps_list:
									for i in range(0,y):
										x = c[i]
										team_id = x['team_id']
										player_id = x['player_id']
										if player_id is None:
											name = x['player_name']
											fps_set = FixturePlayerStat.objects.filter(fps_fixture = f, fps_team__team_id = team_id, fps_player__player_name = name)
										else:
											fps_set = FixturePlayerStat.objects.filter(fps_fixture = f, fps_team__team_id = team_id, fps_player__player_id = player_id)

										if fps_set.exists():
											for_pos = x['formation_position']
											if for_pos is None:
												fps.fps_start = False
											else:
												fps.fps_start = True
											fps.fps_formation_position = x['formation_position']
											fps.fps_position = x['position']
											z = x['stats']
											e = z['cards']
											fps.fps_yellowcards = e['yellowcards']
											fps.fps_redcards = e['redcards']
											e = z['fouls']
											fps.fps_fouls_committed = e['committed']
											fps.fps_fouls_drawn = e['drawn']
											e = z['goals']
											fps.fps_goal_scored = e['scored']
											fps.fps_goal_conceded = e['conceded']
											e = z['other']
											fps.fps_assists = e['assists']
											fps.fps_blocks = e['blocks']
											fps.fps_clearances = e['clearances']
											fps.fps_interceptions = e['interceptions']
											fps.fps_minutes_played = e['minutes_played']
											fps.fps_offsides = e['offsides']
											fps.fps_pen_missed = e['pen_missed']
											fps.fps_pen_scored = e['pen_scored']
											fps.fps_pen_saved = e['pen_saved']
											fps.fps_saves = e['saves']
											fps.fps_tackles = e['tackles']
											e = z['passing']
											fps.fps_passes_total = e['passes']
											fps.fps_passes_accuracy = e['passes_accuracy']
											fps.fps_cross_total = e['total_crosses']
											e = z['shots']
											fps.fps_shots_total = e['shots_total']
											fps.fps_shots_ontarget = e['shots_on_goal']
											fps.fps_shots_offtarget = e['shots_total'] - e['shots_on_goal']
											fps.save()

						else:
							if f.fixture_started == True:
								print('Fixture '+str(f.fixture_id)+' - data added for Fixture Player Statistics for the first time')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['lineup']
								c = b['data']
								b = a['bench']
								e = b['data']
								y = len(e)
								for i in range(0,y):
									c.append(e[i])
								y = len(c)

								for i in range(0,y):
									x = c[i]
									fps = FixturePlayerStat(fps_fixture = f)
									team_id = x['team_id']
									player_id = x['player_id']
									fps.fps_team = Team.objects.get(team_id = team_id)

									if Player.objects.filter(player_id = player_id).exists():
										fps.fps_player = Player.objects.get(player_id = player_id)
									else:
										p = Player(player_id = player_id)
										if player_id is None:
											p.player_team = Team.objects.get(team_id = team_id)
											name = x['player_name']
											p.player_name = x['player_t_name']
											p.save()
											fps.fps_player = Player.objects.get(player_name = name)
										else:
											urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(player_id)+'?api_token='+api_token
											dtwo = json.load(urllib.request.urlopen(urltwo))
											atwo = dtwo['data']
											p.player_team = Team.objects.get(team_id = team_id)
											p.player_name = atwo['fullname']
											p.player_common_name = atwo['common_name']
											p.player_nationality = atwo['nationality']
											p.player_height = atwo['height']
											p.player_weight = atwo['weight']
											p.save()
											fps.fps_player = Player.objects.get(player_id = player_id)

									for_pos = x['formation_position']
									if for_pos is None:
										fps.fps_start = False
									else:
										fps.fps_start = True
									fps.fps_formation_position = x['formation_position']
									fps.fps_position = x['position']
									z = x['stats']
									e = z['cards']
									fps.fps_yellowcards = e['yellowcards']
									fps.fps_redcards = e['redcards']
									e = z['fouls']
									fps.fps_fouls_committed = e['committed']
									fps.fps_fouls_drawn = e['drawn']
									e = z['goals']
									fps.fps_goal_scored = e['scored']
									fps.fps_goal_conceded = e['conceded']
									e = z['other']
									fps.fps_assists = e['assists']
									fps.fps_blocks = e['blocks']
									fps.fps_clearances = e['clearances']
									fps.fps_interceptions = e['interceptions']
									fps.fps_minutes_played = e['minutes_played']
									fps.fps_offsides = e['offsides']
									fps.fps_pen_missed = e['pen_missed']
									fps.fps_pen_scored = e['pen_scored']
									fps.fps_pen_saved = e['pen_saved']
									fps.fps_saves = e['saves']
									fps.fps_tackles = e['tackles']
									e = z['passing']
									fps.fps_passes_total = e['passes']
									fps.fps_passes_accuracy = e['passes_accuracy']
									fps.fps_cross_total = e['total_crosses']
									e = z['shots']
									fps.fps_shots_total = e['shots_total']
									fps.fps_shots_ontarget = e['shots_on_goal']
									if e['shots_total'] is None:
										s_total = 0
									else:
										s_total = e['shots_total']
									if e['shots_on_goal'] is None:
										s_ongoal = 0
									else:
										s_ongoal = e['shots_on_goal']
									fps.fps_shots_offtarget = s_total - s_ongoal
									fps.save()

			# ---------------------- FIXTURE GOAL STATS ------------------------------------------------------------- #

						if Goal.objects.filter(goal_fixture = f).exists():
							if f.fixture_finished == True:
								print('Fixture '+str(f.fixture_id)+' skipped for Fixture Goal Statistics')
								pass
							else:
								print('Fixture '+str(f.fixture_id)+' - data edited for Fixture Goal Statistics')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['goals']
								c = b['data']
								y = len(c)
								goals_list = Goal.objects.filter(goal_fixture = f)

								for goal in goals_list:
									for i in range(0,y):
										x = c[i]
										goal_id = x['id']
										if goal.goal_id == goal_id:
											goal.goal_fixture = f
											team_id = x['team_id']
											scorer_id = x['player_id']
											assist_id = x['player_assist_id']
											assist_name = x['player_assist_name']
											goal.goal_team = Team.objects.get(team_id = team_id)
												
											if scorer_id is None:
												name = x['player_name']
												goal.goal_scorer = Player.objects.get(player_name = name)
											else:
												goal.goal_scorer = Player.objects.get(player_id = scorer_id)
											

											if assist_id is None:
												if assist_name is None:
													pass
												else:
													name = x['player_assist_name']
													goal.goal_assist = Player.objects.get(player_name = name)
											else:
												goal.goal_assist = Player.objects.get(player_id = assist_id)

											goal.goal_minute = x['minute']
											goal.goal_type = x['type']
											goal.save()

						else:
							if f.fixture_started == True:
								print('Fixture '+str(f.fixture_id)+' - data added for Fixture Goal Statistics for the first time')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['goals']
								c = b['data']
								y = len(c)

								for i in range(0,y):
									x = c[i]
									goal = Goal(goal_fixture = f)
									goal.goal_id = x['id']
									team_id = x['team_id']
									scorer_id = x['player_id']
									assist_id = x['player_assist_id']
									assist_name = x['player_assist_name']
									goal.goal_team = Team.objects.get(team_id = team_id)
									
									if Player.objects.filter(player_id = scorer_id).exists():
										goal.goal_scorer = Player.objects.get(player_id = scorer_id)
									else:
										if scorer_id is None:
											p = Player(player_id = 0)
											p.player_team = Team.objects.get(team_id = team_id)
											name = x['player_name']
											p.player_name = x['player_name']
											p.save()
											goal.goal_scorer = Player.objects.get(player_name = name)
										else:
											p = Player(player_id = scorer_id)
											urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(scorer_id)+'?api_token='+api_token
											dtwo = json.load(urllib.request.urlopen(urltwo))
											atwo = dtwo['data']
											p.player_team = Team.objects.get(team_id = team_id)
											p.player_name = atwo['fullname']
											p.player_common_name = atwo['common_name']
											p.player_nationality = atwo['nationality']
											p.player_height = atwo['height']
											p.player_weight = atwo['weight']
											p.save()
											goal.goal_scorer = Player.objects.get(player_id = scorer_id)

									if assist_id is None:
										if assist_name is None:
											pass
										else:
											p = Player(player_id = assist_id)
											p.player_team = Team.objects.get(team_id = team_id)
											name = x['player_name']
											p.player_name = x['player_name']
											p.save()
											goal.goal_assist = Player.objects.get(player_name = name)
									else:
										if Player.objects.filter(player_id = assist_id).exists():
											goal.goal_assist = Player.objects.get(player_id = assist_id)
										else:
											p = Player(player_id = assist_id)
											urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(assist_id)+'?api_token='+api_token
											dtwo = json.load(urllib.request.urlopen(urltwo))
											atwo = dtwo['data']
											p.player_team = Team.objects.get(team_id = team_id)
											p.player_name = atwo['fullname']
											p.player_common_name = atwo['common_name']
											p.player_nationality = atwo['nationality']
											p.player_height = atwo['height']
											p.player_weight = atwo['weight']
											p.save()
											goal.goal_assist = Player.objects.get(player_id = assist_id)

									goal.goal_minute = x['minute']
									goal.goal_type = x['type']
									goal.save()

			# ---------------------- FIXTURE SUBSTITUTION STATS ------------------------------------------------------------- #

						if Substitution.objects.filter(sub_fixture = f).exists():
							if f.fixture_finished == True:
								print('Fixture '+str(f.fixture_id)+' skipped for Fixture Sub Statistics')
								pass
							else:
								print('Fixture '+str(f.fixture_id)+' - data edited for Fixture Sub Statistics')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['substitutions']
								c = b['data']
								y = len(c)
								subs_list = Substitution.objects.filter(sub_fixture = f)

								for sub in subs_list:
									for i in range(0,y):
										x = c[i]
										sub_id = x['id']
										if sub.sub_id == sub_id:
											sub.sub_fixture = f
											team_id = x['team_id']
											in_id = x['player_in_id']
											out_id = x['player_out_id']
											sub.sub_team = Team.objects.get(team_id = team_id)
											if in_id is None:
												name = x['player_in_name']
												sub.sub_in = Player.objects.get(player_name = name)
											else:
												sub.sub_in = Player.objects.get(player_id = in_id)
												
											if out_id is None:
												name = x['player_out_name']
												sub.sub_out = Player.objects.get(player_name = name)
											else:
												sub.sub_out = Player.objects.get(player_id = out_id)
											sub.sub_time = x['minute']
											sub.save()

						else:
							if f.fixture_started == True:
								print('Fixture '+str(f.fixture_id)+' - data added for Fixture Sub Statistics for the first time')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['substitutions']
								c = b['data']
								y = len(c)

								for i in range(0,y):
									x = c[i]
									sub = Substitution(sub_fixture = f)
									sub.sub_id = x['id']
									team_id = x['team_id']
									in_id = x['player_in_id']
									out_id = x['player_out_id']
									sub.sub_team = Team.objects.get(team_id = team_id)

									if Player.objects.filter(player_id = in_id).exists():
										sub.sub_in = Player.objects.get(player_id = in_id)
									else:
										if in_id is None:
											p = Player(player_id = 0)
											p.player_team = Team.objects.get(team_id = team_id)
											name = x['player_in_name']
											p.player_name = x['player_in_name']
											p.save()
											sub.sub_in = Player.objects.get(player_name = name)
										else:
											p = Player(player_id = in_id)
											urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(in_id)+'?api_token='+api_token
											dtwo = json.load(urllib.request.urlopen(urltwo))
											atwo = dtwo['data']
											p.player_team = Team.objects.get(team_id = team_id)
											p.player_name = atwo['fullname']
											p.player_common_name = atwo['common_name']
											p.player_nationality = atwo['nationality']
											p.player_height = atwo['height']
											p.player_weight = atwo['weight']
											p.save()
											sub.sub_in = Player.objects.get(player_id = in_id)

									if Player.objects.filter(player_id = out_id).exists():
										sub.sub_out = Player.objects.get(player_id = out_id)
									else:
										if out_id is None:
											p = Player(player_id = out_id)
											p.player_team = Team.objects.get(team_id = team_id)
											name = x['player_out_name']
											p.player_name = x['player_out_name']
											p.save()
											sub.sub_out = Player.objects.get(player_name = name)
										else:
											p = Player(player_id = out_id)
											urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(out_id)+'?api_token='+api_token
											dtwo = json.load(urllib.request.urlopen(urltwo))
											atwo = dtwo['data']
											p.player_team = Team.objects.get(team_id = team_id)
											p.player_name = atwo['fullname']
											p.player_common_name = atwo['common_name']
											p.player_nationality = atwo['nationality']
											p.player_height = atwo['height']
											p.player_weight = atwo['weight']
											p.save()
											sub.sub_out = Player.objects.get(player_id = out_id)

									sub.sub_time = x['minute']
									sub.save()

			# ---------------------- FIXTURE CARDS STATS ------------------------------------------------------------- #

						if Card.objects.filter(card_fixture = f).exists():
							if f.fixture_finished == True:
								print('Fixture '+str(f.fixture_id)+' skipped for Fixture Card Statistics')
								pass
							else:
								print('Fixture '+str(f.fixture_id)+' - data edited for Fixture Card Statistics')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['cards']
								c = b['data']
								y = len(c)
								cards_list = Card.objects.filter(card_fixture = f)

								for card in cards_list:
									for i in range(0,y):
										x = c[i]
										card_id = x['id']
										if card.card_id == card_id:
											card.card_fixture = f
											team_id = x['team_id']
											player_id = x['player_id']
											card.card_team = Team.objects.get(team_id = team_id)
												
											if player_id is None:
												name = x['player_name']
												card.card_player = Player.objects.get(player_name = name)
											else:
												card.card_player = Player.objects.get(player_id = player_id)
											card.card_time = x['minute']
											card.card_time = x['type']
											card.save()

						else:
							if f.fixture_started == True:
								print('Fixture '+str(f.fixture_id)+' - data added for Fixture Card Statistics for the first time')
								d = json.load(urllib.request.urlopen(url))
								a = d['data']
								b = a['cards']
								c = b['data']
								y = len(c)

								for i in range(0,y):
									x = c[i]
									card = Card(card_fixture = f)
									card.card_id = x['id']
									team_id = x['team_id']
									player_id = x['player_id']
									card.card_team = Team.objects.get(team_id = team_id)

									if Player.objects.filter(player_id = player_id).exists():
										card.card_player = Player.objects.get(player_id = player_id)
									else:
										if player_id is None:
											p = Player(player_id = 0)
											p.player_team = Team.objects.get(team_id = team_id)
											name = x['player_name']
											p.player_name = x['player_name']
											p.save()
											card.card_player = Player.objects.get(player_name = name)
										else:
											p = Player(player_id = player_id)
											urltwo = 'https://soccer.sportmonks.com/api/v2.0/players/'+str(player_id)+'?api_token='+api_token
											dtwo = json.load(urllib.request.urlopen(urltwo))
											atwo = dtwo['data']
											p.player_team = Team.objects.get(team_id = team_id)
											p.player_name = atwo['fullname']
											p.player_common_name = atwo['common_name']
											p.player_nationality = atwo['nationality']
											p.player_height = atwo['height']
											p.player_weight = atwo['weight']
											p.save()
											card.card_player = Player.objects.get(player_id = in_id)
									card.card_type = x['type']
									card.card_time = x['minute']
									card.save()

			print('Data Collection Done')

		else:
			print('No Current Gameweek in Session')

	def handle(self, *args, **options):
		self.populate_fixture_data_objects()		