from django.urls import path
from apps.game.views import GameListCreateView, PlayerListCreateView

app_name = "apps.game"

urlpatterns = [
    path("games/", GameListCreateView.as_view(), name="game-list-create"),
    path("players/", PlayerListCreateView.as_view(), name="player-list-create"),
]
