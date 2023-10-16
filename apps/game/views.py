from rest_framework import status
from rest_framework.views import APIView
from apps.game.models import Game, Player
from apps.game.serializers import GameSerializer, PlayerSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.views import extend_schema
from rest_framework.response import Response


class GameList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get a list of games",
        description="Retrieve a list of all available games.",
    )
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(
            data={"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class CreateGame(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        summary="Create a new game",
        description="Create a new game with the provided data.",
    )
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": "success",
                    "message": "Game created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class GameDetail(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get game details",
        description="Retrieve details of a specific game by its ID.",
    )
    def get(self, request, id):
        try:
            game = Game.objects.get(id=id)
            serializer = GameSerializer(game)
            return Response(
                data={"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Game.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Game not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UpdateGame(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        summary="Update game details",
        description="Update details of a specific game by its ID.",
    )
    def put(self, request, id):
        try:
            game = Game.objects.get(id=id)
            serializer = GameSerializer(game, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data={"status": "success", "message": "Game updated successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Game.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Game not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class DeleteGame(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        summary="Delete a game",
        description="Delete a specific game by its ID.",
    )
    def delete(self, request, id):
        try:
            game = Game.objects.get(id=id)
            game.delete()
            return Response(
                data={"status": "success", "message": "Game deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Game.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Game not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PlayerList(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get a list of players",
        description="Retrieve a list of all players.",
    )
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(
            data={"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class CreatePlayer(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new player",
        description="Create a new player using provided data.",
    )
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={
                    "status": "success",
                    "message": "Player created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class PlayerDetail(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get player details",
        description="Retrieve details of a player by player ID.",
    )
    def get(self, request, id):
        try:
            player = Player.objects.get(id=id)
            serializer = PlayerSerializer(player)
            return Response(
                data={"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Player.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Player not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Update player details",
        description="Update details of a player by player ID.",
    )
    def put(self, request, id):
        try:
            player = Player.objects.get(id=id)
            serializer = PlayerSerializer(player, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data={
                        "status": "success",
                        "message": "Player updated successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Player.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Player not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Delete a player",
        description="Delete a player by player ID.",
    )
    def delete(self, request, id):
        try:
            player = Player.objects.get(id=id)
            player.delete()
            return Response(
                data={"status": "success", "message": "Player deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Player.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Player not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UpdatePlayer(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update player details",
        description="Update details of a player by player ID.",
    )
    def put(self, request, id):
        try:
            player = Player.objects.get(id=id)
            serializer = PlayerSerializer(player, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data={
                        "status": "success",
                        "message": "Player updated successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                data={
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Player.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Player not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class DeletePlayer(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Delete a player",
        description="Delete a player by player ID.",
    )
    def delete(self, request, id):
        try:
            player = Player.objects.get(id=id)
            player.delete()
            return Response(
                data={"status": "success", "message": "Player deleted successfully"},
                status=status.HTTP_200_OK,
            )
        except Player.DoesNotExist:
            return Response(
                data={"status": "error", "message": "Player not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
