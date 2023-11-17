from django.contrib import admin
from apps.game.models import Game, Player


class GameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ["name"]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("user", "experience_level", "created_at")
    list_filter = list_display
    search_fields = ["user__username"]


admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
