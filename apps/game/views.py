from rest_framework import generics
from rest_framework.views import APIView
from apps.game.models import Game, Player
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.game.serializers import GameSerializer, PlayerSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status


class GamesList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
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


class CreateGame(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request: Request):
        """
        POST method to create a new game
        """
        data = request.data
        serializer = GameSerializer(data=data)

        if serializer.is_valid:
            serializer.save()
            response = {
                "status": "success",
                "message": "Game created successfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_request_response = {
            "status": "failed",
            "message": "Game not created",
            "error_message": serializer.errors,
        }
        return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)


# Create similar views for Player
class PlayerListCreateView(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
