from django.contrib import admin
from .models import Match, Bet, Outcome


class MatchAdmin(admin.ModelAdmin):
    list_display = ("match_date", "status", "player_1", "player_2", "duration_minutes")
    list_filter = ("status",)
    search_fields = ("player_1__username", "player_2__username", "notes")
    date_hierarchy = "match_date"


class BetAdmin(admin.ModelAdmin):
    list_display = ("match", "amount", "is_winner")
    list_filter = ("is_winner",)
    search_fields = ("match__player_1__username", "match__player_2__username")


class OutcomeAdmin(admin.ModelAdmin):
    list_display = ("match", "winner", "loser", "winning_amount")
    search_fields = (
        "match__player_1__username",
        "match__player_2__username",
        "winner__username",
        "loser__username",
    )


admin.site.register(Match, MatchAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Outcome, OutcomeAdmin)
