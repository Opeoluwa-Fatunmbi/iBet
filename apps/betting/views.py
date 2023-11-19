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
from apps.mediation.models import Mediator
from apps.billing.serializers import WalletSerializer


# betting/views

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
"""

## Should the match and bet views be combined?


class BetCreateView(APIView):
    serializer_class = CreateMatchSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Create a new match",
        description="Create a new match with two players and a mediator.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    amount = serializer.validated_data["amount"]
                    game = serializer.validated_data["game"]

                    # Find two available players dynamically based on criteria
                    available_players = Player.objects.filter(
                        amount=amount, game=game, is_engaged=False
                    )

                    available_mediator = Mediator.objects.filter(
                        is_engaged=False
                    ).first()

                    # Check if there are available players and a mediator
                    if available_players.exists() and available_mediator:
                        # Select two random players
                        players = available_players.order_by("?")[:2]

                        # Create the match
                        match = Match.objects.create(
                            player_1=players[0],
                            player_2=players[1],
                            mediator=available_mediator,
                            amount=amount,
                            game=game,
                            is_occupied=True,
                        )

                        # Update players and mediator to be engaged
                        players.update(is_engaged=True)
                        available_mediator.is_engaged = True
                        available_mediator.save()

                        return CustomResponse.success(
                            self.serializer_class(match).data, status=201
                        )
                    else:
                        return CustomResponse.error(
                            {"error": "No available players or mediator."}, status=400
                        )

                return CustomResponse.error(serializer.errors, status=400)
        except Exception as e:
            return CustomResponse.error({"error": str(e)}, status=500)


class BetDetailView(APIView):
    serializer_class = MatchSerializer

    @extend_schema(
        summary="Get a match",
        description="Get a match with the player_1, player_2, and mediator.",
    )
    def get(self, request, pk):
        try:
            match = Match.objects.get(pk=pk)
            serializer = self.serializer_class(match)
            return CustomResponse.success(serializer.data, status=200)

        except Match.DoesNotExist:
            return CustomResponse.error("Match does not exist", status=404)


class BetListView(APIView):
    serializer_class = MatchSerializer

    @extend_schema(
        summary="Available matches", description="Get the list of all available matches"
    )
    def get(self, request):
        matches = Match.objects.all()
        serializer = self.serializer_class(matches, many=True)
        if serializer.is_valid(raise_exception=True):
            return CustomResponse.success(serializer.data, status=200)
        return CustomResponse.error(serializer.errors, status=404)


class ConfirmOutcomeView(APIView):
    serializer_class = OutcomeSerializer

    @extend_schema(
        summary="Confirm outcome",
        description="Confirm the outcome of a match and update the players and mediator.",
    )
    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    winner = serializer.validated_data["winner"]
                    loser = serializer.validated_data["loser"]

                    match = Match.objects.get(pk=pk)

                    # Ensure that the match is not already confirmed
                    if match.status == Match.MATCH_STATUS_CHOICES.PENDING:
                        # Update the match status
                        match.status = Match.MATCH_STATUS_CHOICES.COMPLETED
                        match.save()

                        # Update the players and mediator
                        match.player_1.is_engaged = False
                        match.player_2.is_engaged = False
                        match.mediator.is_engaged = False

                        # Determine the amounts based on your specified rules
                        winner_amount = match.amount + 0.8 * match.player_2.amount
                        loser_amount = 0.2 * match.player_2.amount
                        mediator_amount = 0.1 * match.amount

                        # Update the winner's amount
                        match.player_1.amount += winner_amount

                        # Update the loser's amount
                        match.player_2.amount -= loser_amount

                        # Update the mediator's amount
                        match.mediator.amount += mediator_amount

                        # Save the players and mediator
                        match.player_1.save()
                        match.player_2.save()
                        match.mediator.save()

                        # Optionally, update wallet balances
                        winner_wallet_serializer = WalletSerializer(
                            match.player_1.wallet,
                            data={"balance": match.player_1.amount},
                        )
                        if winner_wallet_serializer.is_valid():
                            winner_wallet_serializer.save()

                        loser_wallet_serializer = WalletSerializer(
                            match.player_2.wallet,
                            data={"balance": match.player_2.amount},
                        )
                        if loser_wallet_serializer.is_valid():
                            loser_wallet_serializer.save()

                        mediator_wallet_serializer = WalletSerializer(
                            match.mediator.wallet,
                            data={"balance": match.mediator.amount},
                        )
                        if mediator_wallet_serializer.is_valid():
                            mediator_wallet_serializer.save()

                        return CustomResponse.success(
                            self.serializer_class(match).data, status=200
                        )
                    else:
                        return CustomResponse.error(
                            {"error": "Match outcome already confirmed."}, status=400
                        )

                return CustomResponse.error(serializer.errors, status=400)
        except Exception as e:
            return CustomResponse.error({"error": str(e)}, status=500)


class ListOutcomesView(APIView):
    serializer_class = OutcomeSerializer

    @extend_schema(
        summary="List outcomes",
        description="List all outcomes for a match.",
    )
    def get(self, request, pk):
        try:
            match = Match.objects.get(pk=pk)
            outcomes = Outcome.objects.filter(match=match)
            serializer = self.serializer_class(outcomes, many=True)
            return CustomResponse.success(serializer.data, status=200)

        except Match.DoesNotExist:
            return CustomResponse.error("Match does not exist", status=404)
