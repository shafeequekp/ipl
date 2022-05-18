from django.contrib import admin

from applications.match.models import Team, Player, Match, Venue, Season, City, Umpire, Delivery


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']


class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'match_winner', 'player_of_the_match', )
    list_filter = ['season', ]


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'total_runs', 'player_dismissed', 'dismissal_kind', ]


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(City)
admin.site.register(Venue)
admin.site.register(Season)
admin.site.register(Umpire)
admin.site.register(Delivery, DeliveryAdmin)
