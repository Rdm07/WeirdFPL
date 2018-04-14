from django.contrib import admin
from django.utils import timezone
from Statistics.models import *

# Register your models here.

admin.site.site_header = 'WFPL Site Administration'

class SeasonAdmin(admin.ModelAdmin):
	model = Season
	list_display = ('season_name', 'is_current')

class GameweekAdmin(admin.ModelAdmin):
	model = Gameweek
	list_display = ('gw_number', 'gw_season', 'gw_start', 'gw_end')
	search_fields = ('gw_season__season_name', 'gw_number')
	ordering = ('gw_season__season_name', 'gw_number')

class VenueAdmin(admin.ModelAdmin):
	model = Venue
	list_display = ('venue_name', 'venue_capacity')

class TeamAdmin(admin.ModelAdmin):
	model = Team
	list_display = ('team_name', 'team_id')
	search_fields = ('team_name', 'team_id')
	ordering = ('team_name', 'team_id')

class FixtureAdmin(admin.ModelAdmin):
	model = Fixture
	list_display = ('fixture_gameweek', 'fixture_team_home', 'fixture_team_away', 'fixture_ft_score')
	search_fields = ('fixture_id', 'fixture_gameweek__gw_number', 'fixture_team_home__team_name', 'fixture_team_away__team_name')
	ordering = ('fixture_gameweek__gw_number', 'fixture_team_home__team_name')

class FixtureTeamStatAdmin(admin.ModelAdmin):
	model = FixtureTeamStat
	list_display = ('fts_team', 'get_gameweek', 'fts_team_type', 'fts_fixture')
	search_fields = ('fts_team__team_name', 'fts_team_type', 'fts_fixture__fixture_id')
	ordering = ('fts_team__team_name', 'fts_fixture__fixture_gameweek', 'fts_team_type')

	def get_gameweek(self, obj):
		return obj.fts_fixture.fixture_gameweek.gw_number
	get_gameweek.short_description = 'Gameweek'
	
class PlayerAdmin(admin.ModelAdmin):
	model = Player
	list_display = ('player_common_name', 'player_team', 'player_name')
	search_fields = ('player_name', 'player_team__team_name')
	ordering = ('player_team__team_name', 'player_common_name')


class GoalAdmin(admin.ModelAdmin):
	model = Goal
	list_display = ('goal_fixture', 'goal_team', 'goal_scorer', 'goal_assist', 'goal_type')
	search_fields = ('goal_team__team_name', 'goal_scorer__player_name', 'goal_assist__player_name', 'goal_fixture__fixture_id')
	ordering = ('goal_fixture', 'goal_team', 'goal_scorer', 'goal_assist')

class SubstitutionAdmin(admin.ModelAdmin):
	model = Substitution
	list_display = ('sub_fixture', 'sub_team', 'sub_in', 'sub_out')
	search_fields = ('sub_fixture__fixture_id', 'sub_team__team_name', 'sub_in__player_name', 'sub_out__player_name')
	ordering = ('sub_fixture', 'sub_team')

class FixturePlayerStatAdmin(admin.ModelAdmin):
	model = FixturePlayerStat
	list_display = ('fps_player', 'get_gameweek', 'fps_fixture', 'fps_team')
	search_fields = ('fps_team__team_name', 'fps_player__player_name', 'fps_fixture__fixture_id')
	ordering = ('fps_fixture__fixture_gameweek', 'fps_team__team_name', 'fps_player__player_name')

	def get_gameweek(self, obj):
		return obj.fps_fixture.fixture_gameweek.gw_number
	get_gameweek.short_description = 'Gameweek'

class CardAdmin(admin.ModelAdmin):
	model = Substitution
	list_display = ('card_id', 'card_fixture', 'card_team', 'card_player', 'card_type')
	search_fields = ('card_fixture__fixture_id', 'card_team__team_name', 'card_player__player_name', 'card_type')
	ordering = ('card_fixture', 'card_team')

# -------------------------------------------------------------------------------------------------

admin.site.register(Season, SeasonAdmin)
admin.site.register(Gameweek, GameweekAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(FixtureTeamStat, FixtureTeamStatAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Substitution, SubstitutionAdmin)
admin.site.register(FixturePlayerStat, FixturePlayerStatAdmin)
admin.site.register(Card, CardAdmin)