from django.urls import path
from .views import (
    GameList,
    CreateGame,
    GameDetail,
    UpdateGame,
    DeleteGame,
    PlayerList,
    CreatePlayer,
    PlayerDetail,
    UpdatePlayer,
    DeletePlayer,
)

urlpatterns = [
    path("games/", GameList.as_view(), name="game-list"),
    path("games/create/", CreateGame.as_view(), name="create-game"),
    path("games/<uuid:id>/", GameDetail.as_view(), name="game-detail"),
    path("games/<uuid:id>/update/", UpdateGame.as_view(), name="update-game"),
    path("games/<uuid:id>/delete/", DeleteGame.as_view(), name="delete-game"),
    path("players/", PlayerList.as_view(), name="player-list"),
    path("players/create/", CreatePlayer.as_view(), name="create-player"),
    path("players/<uuid:id>/", PlayerDetail.as_view(), name="player-detail"),
    path("players/<uuid:id>/update/", UpdatePlayer.as_view(), name="update-player"),
    path("players/<uuid:id>/delete/", DeletePlayer.as_view(), name="delete-player"),
]
