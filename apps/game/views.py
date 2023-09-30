from rest_framework import generics
from rest_framework.views import APIView
from apps.game.models import Game, Player
from rest_framework.permissions import IsAuthenticated
from apps.game.serializers import GameSerializer, PlayerSerializer
from rest_framework.response import Response


class GamesList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)
        if serializer.is_valid:
            return Response(data=serializer.data, status=401)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Game
from .serializers import GameSerializer  # Make sure to import your serializer


class GamesList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)

        if serializer.is_valid:
            # Return a response with a 200 status code for a successful GET request
            return Response(
                data={
                    "status": "success",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "status": "error",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


# Create similar views for Player
class PlayerListCreateView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
