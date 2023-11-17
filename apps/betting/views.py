from rest_framework.views import APIView
from apps.betting.models import Match, Bet, Outcome
from .serializers import (
    CreateMatchSerializer,
    BetSerializer,
    OutcomeSerializer,
    MatchSerializer,
)
from apps.core.responses import CustomResponse
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema
from django.db import transaction
from apps.game.models import Player
from django.db.models import Q


# betting/views
class CreateMatchView(APIView):
    serializer_class = CreateMatchSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Create a new match",
        description="Create a new match with the player_1, player_2, and mediator.",
    )
    def get(self, request):
        matches = Match.objects.all()
        serializer = self.serializer_class(matches, many=True)
        return CustomResponse.success(serializer.data, status=200)


"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    # Look for players with same stake amount and game
                    query = Player.objects.filter(Q(amount=serializer.data['amount']) & Q (game=serializer.data['game']) )

                    serializer.save()
                    return CustomResponse.success(serializer.data, status=201)
                return CustomResponse.error(serializer.errors, status=404)
        except Exception as e:
            return CustomResponse.error(str(e), status=404)
"""


class BetCreateView(APIView):
    serializer_class = BetSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Create a new match",
        description="Create a new match with the player_1, player_2, and mediator.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(serializer.data, status=201)

        return CustomResponse.error(serializer.errors, status=404)


class BetDetailView(APIView):
    serializer_class = BetSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Create a new match",
        description="Create a new match with the player_1, player_2, and mediator.",
    )
    def get(self, request, pk):
        try:
            bet = Bet.objects.get(pk=pk)
            serializer = self.serializer_class(bet)
            return CustomResponse.success(serializer.data, status=200)

        except Bet.DoesNotExist:
            return CustomResponse.error("Bet does not exist", status=404)


class BetListView(APIView):
    serializer_class = BetSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Available bets", description="Get the list of all available bets"
    )
    def get(self, request):
        bets = Bet.objects.all()
        serializer = self.serializer_class(bets, many=True)
        return CustomResponse.success(serializer.data, status=200)


class ConfirmOutcomeView(APIView):
    pass


class OutcomeView(APIView):
    pass
