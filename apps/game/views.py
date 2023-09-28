from rest_framework import generics
from apps.game.models import Game, Player
from apps.game.serializers import GameSerializer, PlayerSerializer


class GameListCreateView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# Create similar views for Player
class PlayerListCreateView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
