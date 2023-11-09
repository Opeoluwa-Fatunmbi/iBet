from django.contrib import admin
from apps.betting.models import *

# Register your models here.
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_date', 'location', 'status', 'winner', 'loser')
    list_filter = ('status',)
    search_fields = ('location', 'winner__username', 'loser__username')
    list_per_page = 20

class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'amount', 'is_winner')
    list_filter = ('is_winner',)
    search_fields = ('user__username', 'match__location')
    list_per_page = 20

class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('match', 'winner', 'winning_amount')
    list_filter = ('winner',)
    search_fields = ('match__location', 'winner__username')
    list_per_page = 20



admin.site.register(Bet, BetAdmin)
admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(Match, MatchAdmin)
