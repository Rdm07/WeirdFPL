from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models


# Create your models here.

class Season(models.Model):
	season_id = models.IntegerField(null=True)
	season_name = models.CharField(max_length = 10)
	is_current = models.BooleanField(default=False)

	def __str__(self):
		return str(self.season_name)

class Gameweek(models.Model):
	gw_id = models.IntegerField(null=True)
	gw_number = models.IntegerField(null=True)
	gw_start = models.DateField()
	gw_end = models.DateField()
	gw_season = models.ForeignKey(Season, on_delete=models.CASCADE)

	@property
	def gw_started(self):
		if timezone.now().date() >= self.gw_start:
			return True
		return False

	@property
	def gw_finished(self):
		if timezone.now().date() > self.gw_end:
			return True
		return False

	def __str__(self):
		return str(self.gw_number)

class Venue(models.Model):
	venue_id = models.IntegerField(null=True)
	venue_name = models.CharField(max_length = 50)
	venue_city = models.CharField(max_length = 50)
	venue_capacity = models.IntegerField(null=True)

	def __str__(self):
		return str(self.venue_name)

class Team(models.Model):
	team_id = models.IntegerField(null=True)
	team_name = models.CharField(max_length = 50)
	team_venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	# team_logo = models.ImageField(upload_to = 'team_logo')

	def __str__(self):
		return str(self.team_name)

class Fixture(models.Model):
	fixture_id = models.IntegerField(null=True)
	fixture_gameweek = models.ForeignKey(Gameweek, on_delete=models.CASCADE)
	fixture_venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	fixture_start = models.DateTimeField(auto_now=False, auto_now_add=False)
	fixture_team_home = models.ForeignKey(Team, related_name = 'Home_Team', on_delete=models.CASCADE)
	fixture_team_away = models.ForeignKey(Team, related_name = 'Away_Team', on_delete=models.CASCADE)
	fixture_ht_score = models.CharField(max_length = 5, null = True)
	fixture_ft_score = models.CharField(max_length = 5, null = True)

	@property
	def fixture_finished(self):
		if (timezone.now() - self.fixture_start) > timedelta(hours=2):
			return True
		return False

	@property
	def fixture_started(self):
		if timezone.now() > self.fixture_start:
			return True
		return False

	def __str__(self):
		return str(self.fixture_team_home.team_name)+' v. '+str(self.fixture_team_away.team_name)

class FixtureTeamStat(models.Model):
	fts_fixture = models.ForeignKey(Fixture, related_name = 'Fixture_Team_Stats', on_delete=models.CASCADE)
	fts_team = models.ForeignKey(Team, related_name = 'Team_Details', on_delete=models.CASCADE)
	fts_team_type = models.CharField(max_length = 5, choices = (('Home','Home'), ('Away','Away'), ))
	fts_formation = models.CharField(max_length = 10)
	fts_score = models.IntegerField(null=True)
	# fts_coach = models.ForeignKey
	fts_corners = models.IntegerField(null = True)
	fts_fouls_committed = models.IntegerField(null = True)
	fts_fouls_drawn = models.IntegerField(null = True) # freekick in the stats
	fts_goalkicks = models.IntegerField(null = True)
	fts_offsides = models.IntegerField(null = True)
	fts_passes_total = models.IntegerField(null = True)
	fts_passes_accuracy = models.IntegerField(null = True)
	fts_possession = models.IntegerField(null = True)
	fts_yellowcards = models.IntegerField(null = True)
	fts_redcards = models.IntegerField(null = True)
	fts_saves = models.IntegerField(null = True)
	fts_shots_total = models.IntegerField(null = True)
	fts_shots_ontarget = models.IntegerField(null = True)
	fts_shots_offtarget = models.IntegerField(null = True)
	fts_shots_blocked = models.IntegerField(null = True)
	fts_shots_insidebox = models.IntegerField(null = True)
	fts_shots_outsidebox = models.IntegerField(null = True)
	fts_substitutions = models.IntegerField(null = True)
	
	def __str__(self):
		return str(self.fts_team)+'_'+str(self.fts_fixture.fixture_gameweek.gw_number)

class Player(models.Model):
	player_id = models.IntegerField()
	player_name = models.CharField(max_length = 50)
	player_common_name = models.CharField(max_length = 50, null = True)
	player_team = models.ForeignKey(Team, related_name = 'Player_Team', on_delete=models.CASCADE)
	player_nationality = models.CharField(max_length = 15, null = True)
	player_height = models.CharField(max_length = 10, null = True)
	player_weight = models.CharField(max_length = 10, null = True)
	# player_photo = models.ImageField(upload_to = 'player_logo')

	def __str__(self):
		return str(self.player_common_name)

class Goal(models.Model):
	goal_id = models.IntegerField(null = True)
	goal_fixture = models.ForeignKey(Fixture, related_name = 'Goal_Fixture', on_delete=models.CASCADE)
	goal_team = models.ForeignKey(Team, related_name = 'Goal_Team', on_delete=models.CASCADE)
	goal_scorer = models.ForeignKey(Player, related_name = 'Goal_Scorer', on_delete=models.CASCADE)
	goal_assist = models.ForeignKey(Player, related_name = 'Goal_Assist', on_delete=models.CASCADE, null = True)
	goal_minute = models.IntegerField(null = True)
	goal_type = models.CharField(max_length=10)

	def __str__(self):
		return str(self.goal_scorer)

class Substitution(models.Model):
	sub_id = models.IntegerField(null = True)
	sub_fixture = models.ForeignKey(Fixture, related_name = 'Sub_Fixture', on_delete=models.CASCADE)
	sub_team = models.ForeignKey(Team, related_name = 'Sub_Team', on_delete=models.CASCADE)
	sub_in = models.ForeignKey(Player, related_name = 'Sub_In', on_delete=models.CASCADE)
	sub_out = models.ForeignKey(Player, related_name = 'Sub_Out', on_delete=models.CASCADE, null = True)
	sub_time = models.IntegerField(null = True)

	def __str__(self):
		return str(self.sub_team)

class FixturePlayerStat(models.Model):
	fps_fixture = models.ForeignKey(Fixture, related_name = 'Fixture_Player_Stats', on_delete=models.CASCADE)
	fps_team = models.ForeignKey(Team, related_name = 'Player_Team_Stat', on_delete=models.CASCADE)
	fps_player = models.ForeignKey(Player, related_name = 'Stat_Player', on_delete=models.CASCADE)
	fps_start = models.BooleanField()
	fps_formation_position = models.IntegerField(null = True)
	fps_position = models.CharField(max_length=5)
	fps_yellowcards = models.IntegerField(null = True)
	fps_redcards = models.IntegerField(null = True)
	fps_fouls_committed = models.IntegerField(null = True)
	fps_fouls_drawn = models.IntegerField(null = True)
	fps_goal_scored = models.IntegerField(null = True)
	fps_goal_conceded = models.IntegerField(null = True)
	fps_assists = models.IntegerField(null = True)
	fps_blocks = models.IntegerField(null = True)
	fps_clearances = models.IntegerField(null = True)
	fps_interceptions = models.IntegerField(null = True)
	fps_minutes_played = models.IntegerField(null = True)
	fps_offsides = models.IntegerField(null = True)
	fps_pen_missed = models.IntegerField(null = True)
	fps_pen_scored = models.IntegerField(null = True)
	fps_pen_saved = models.IntegerField(null = True)
	fps_saves = models.IntegerField(null = True)
	fps_tackles = models.IntegerField(null = True)
	fps_passes_total = models.IntegerField(null = True)
	fps_passes_accuracy = models.IntegerField(null = True)
	fps_cross_total = models.IntegerField(null = True)
	fps_shots_total = models.IntegerField(null = True)
	fps_shots_ontarget = models.IntegerField(null = True)
	fps_shots_offtarget = models.IntegerField(null = True)
	
	def __str__(self):
		return str(self.fps_player.player_common_name)+'_'+str(self.fps_fixture)

class Card(models.Model):
	card_id = models.IntegerField(null = True)
	card_fixture = models.ForeignKey(Fixture, related_name = 'Card_Fixture', on_delete=models.CASCADE)
	card_team = models.ForeignKey(Team, related_name = 'Card_Team', on_delete=models.CASCADE)
	card_type = models.CharField(max_length=10)
	card_player = models.ForeignKey(Player, related_name = 'Card', on_delete=models.CASCADE, null = True)
	card_time = models.IntegerField(null = True)

	def __str__(self):
		return str(self.card_team)