from django.contrib import admin
from .models import Game, Player


class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "min_players", "max_players", "is_active")
    list_filter = list_display
    search_fields = ["name"]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "experience_level")
    list_filter = list_display
    search_fields = ["user__username"]


admin.site.register(Game)
admin.site.register(Player)
