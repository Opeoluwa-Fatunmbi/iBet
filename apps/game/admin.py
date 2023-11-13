from django.contrib import admin
from apps.game.models import Game, Player

# Register your models here.


class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "game", "min_players", "max_players", "is_active")
    list_filter = ("game", "is_active")
    search_fields = ("name",)
    ordering = ("id",)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "score", "experience_level")
    search_fields = ("user__username", "user__email")
    ordering = ("id",)


admin.register(Game, GameAdmin)
admin.register(Player, PlayerAdmin)
