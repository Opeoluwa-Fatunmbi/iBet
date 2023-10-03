from django.urls import path
from apps.game.views import CreateGame, PlayerListCreateView, GamesList

app_name = "apps.game"

urlpatterns = [
    path("", GamesList.as_view(), name="game-list"),
    path("create-game/", CreateGame.as_view(), name="create-game"),
    path("players/", PlayerListCreateView.as_view(), name="player-list-create"),
]
