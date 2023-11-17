from rest_framework import status
from rest_framework.views import APIView
from apps.game.models import Game, Player
from apps.game.serializers import GameSerializer, PlayerSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.views import extend_schema
from apps.core.responses import CustomResponse


class GameList(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer

    @extend_schema(
        summary="Get a list of games",
        description="Retrieve a list of all available games.",
    )
    def get(self, request):
        try:
            games = Game.objects.all()
            serializer = GameSerializer(games, many=True)
            return CustomResponse.success(
                message="Request successful",
                data=serializer.data,
                status_code=200,
            )

        except Exception as e:
            return CustomResponse.error(
                message="An error occurred",
                data=str(e),
                status_code=500,
            )


class CreateGame(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        summary="Create a new game",
        description="Create a new game with the provided data.",
    )
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data={
                    "status": "success",
                    "message": "Game created successfully",
                    "data": serializer.data,
                },
                status=201,
            )
        return CustomResponse.error(
            data={
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=400,
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
            return CustomResponse.success(
                data={"status": "success", "data": serializer.data},
                status=200,
            )
        except Game.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Game not found"},
                status=404,
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
                return CustomResponse.success(
                    data={"status": "success", "message": "Game updated successfully"},
                    status=200,
                )
            return CustomResponse.error(
                data={
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=400,
            )
        except Game.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Game not found"},
                status=404,
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
            return CustomResponse.success(
                data={"status": "success", "message": "Game deleted successfully"},
                status=200,
            )
        except Game.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Game not found"},
                status=404,
            )


class PlayerList(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get a list of players",
        description="Retrieve a list of all players.",
    )
    def get(self, request):
        try:
            players = Player.objects.all()
            serializer = PlayerSerializer(players, many=True)
            return CustomResponse.success(
                message="Request successful",
                data=serializer.data,
                status_code=200,
            )
        except Exception as e:
            return CustomResponse.error(
                message="An error occurred",
                data=str(e),
                status_code=500,
            )


class CreatePlayer(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create a new player",
        description="Create a new player using provided data.",
    )
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data={
                    "status": "success",
                    "message": "Player created successfully",
                    "data": serializer.data,
                },
                status=201,
            )
        return CustomResponse.error(
            data={
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=400,
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
            return CustomResponse.success(
                data={"status": "success", "data": serializer.data},
                status=200,
            )
        except Player.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Player not found"},
                status=404,
            )

    @extend_schema(
        summary="Update player details",
        description="Update details of a player by player ID.",
    )
    def put(self, request, id):
        try:
            player = Player.objects.get(id=id)
            serializer = PlayerSerializer(player, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse.success(
                    data={
                        "status": "success",
                        "message": "Player updated successfully",
                    },
                    status=200,
                )
            return CustomResponse.error(
                data={
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=400,
            )
        except Player.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Player not found"},
                status=404,
            )

    @extend_schema(
        summary="Delete a player",
        description="Delete a player by player ID.",
    )
    def delete(self, request, id):
        try:
            player = Player.objects.get(id=id)
            player.delete()
            return CustomResponse.success(
                data={"status": "success", "message": "Player deleted successfully"},
                status=200,
            )
        except Player.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Player not found"},
                status=404,
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
                return CustomResponse.success(
                    data={
                        "status": "success",
                        "message": "Player updated successfully",
                    },
                    status=200,
                )
            return CustomResponse.error(
                data={
                    "status": "error",
                    "message": "Invalid data",
                    "errors": serializer.errors,
                },
                status=400,
            )
        except Player.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Player not found"},
                status=404,
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
            return CustomResponse.success(
                data={"status": "success", "message": "Player deleted successfully"},
                status=200,
            )
        except Player.DoesNotExist:
            return CustomResponse.error(
                data={"status": "error", "message": "Player not found"},
                status=404,
            )
