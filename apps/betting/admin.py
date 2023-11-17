from django.contrib import admin
from apps.betting.models import Match, Bet, Outcome


class MatchAdmin(admin.ModelAdmin):
    list_display = ("status", "player_1", "player_2", "duration_minutes")
    list_filter = ("status",)
    search_fields = ("player_1__username", "player_2__username", "notes")
    date_hierarchy = "created_at"


class BetAdmin(admin.ModelAdmin):
    list_display = ("amount",)
    list_filter = list_display


class OutcomeAdmin(admin.ModelAdmin):
    list_display = ("match", "winner", "loser", "amount")
    search_fields = (
        "match__player_1__username",
        "match__player_2__username",
        "winner__username",
        "loser__username",
    )


admin.site.register(Match, MatchAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Outcome, OutcomeAdmin)
