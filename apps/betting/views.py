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
from apps.mediation.models import Mediator
from apps.billing.serializers import WalletSerializer
from rest_framework.permissions import IsAuthenticated
from apps.betting.permissions import IsPlayer


# betting/views.py
class CreateBetView(APIView):
    serializer_class = BetSerializer
    throttle_classes = [UserRateThrottle]
    # permission_classes = [IsAuthenticated, IsPlayer]

    @extend_schema(
        summary="Create a new bet",
        description="Create a new bet with a specified amount and game.",
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        try:
            if serializer.is_valid(raise_exception=True):
                amount = serializer.validated_data["amount"]
                game = serializer.validated_data["game"]

                # Deduct amount from the user's wallet
                user = request.user
                user_wallet = user.wallet
                if user_wallet.balance < amount:
                    return CustomResponse.error(
                        {"error": "Insufficient balance."}, status=400
                    )
                user_wallet.balance -= amount
                user_wallet.save()

                # Create the bet
                serializer.save()

                # Set is_active to True for the player
                user.player.is_active = True
                user.player.save()

                return CustomResponse.success(serializer.data, status=201)
            else:
                return CustomResponse.error({"error": "Invalid data."}, status=400)

        except Exception as e:
            return CustomResponse.error({"error": str(e)}, status=500)


class BetDetailView(APIView):
    serializer_class = BetSerializer

    @extend_schema(
        summary="Get a match",
        description="Get a match with the player_1, player_2, and mediator.",
    )
    def get(self, request, pk):
        try:
            match = Bet.objects.get(pk=pk)
            serializer = self.serializer_class(match)
            return CustomResponse.success(serializer.data, status=200)

        except Match.DoesNotExist:
            return CustomResponse.error("Match does not exist", status=404)


class BetListView(APIView):
    serializer_class = BetSerializer

    @extend_schema(
        summary="Available matches", description="Get the list of all available matches"
    )
    def get(self, request):
        matches = Bet.objects.all()
        serializer = self.serializer_class(matches, many=True)
        if serializer.is_valid(raise_exception=True):
            return CustomResponse.success(serializer.data, status=200)
        return CustomResponse.error(serializer.errors, status=404)


class DeleteBetView(APIView):
    serializer_class = BetSerializer

    @extend_schema(
        summary="Delete a bet",
        description="Delete a bet with the specified id.",
    )
    def delete(self, request, pk):
        try:
            bet = Bet.objects.get(pk=pk)
            bet.delete()
            return CustomResponse.success("Bet deleted successfully.", status=200)
        except Bet.DoesNotExist:
            return CustomResponse.error("Bet does not exist", status=404)


class CreateMatchView(APIView):
    serializer_class = MatchSerializer
    throttle_classes = [UserRateThrottle]
    # permission_classes = [IsAuthenticated, IsPlayer]

    @extend_schema(
        summary="Create a new match",
        description="Create a new match with two players and a mediator.",
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        try:
            if serializer.is_valid(raise_exception=True):
                amount = serializer.validated_data["amount"]
                game = serializer.validated_data["game"]

                # Find two available players dynamically based on criteria
                available_players = Player.objects.filter(
                    amount=amount, game=game, is_active=True
                )

                # Find an available mediator
                available_mediator = Mediator.objects.filter(is_active=False).first()

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
                        is_active=True,
                    )

                    # Update players and mediator to be engaged
                    players.update(is_active=True)
                    available_mediator.is_active = True
                    available_mediator.is_active = True
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


class MatchDetailView(APIView):
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


class MatchListView(APIView):
    serializer_class = MatchSerializer

    @extend_schema(
        summary="Available matches", description="Get the list of all available matches"
    )
    def get(self, request):
        matches = Match.objects.filter(is_active=True)
        serializer = self.serializer_class(matches, many=True)
        if serializer.is_valid(raise_exception=True):
            return CustomResponse.success(serializer.data, status=200)
        return CustomResponse.error(serializer.errors, status=404)


class UpdateMatchView(APIView):
    serializer_class = MatchSerializer

    @extend_schema(
        summary="Update a match",
        description="Update a match with the specified id.",
    )
    def put(self, request, pk):
        try:
            match = Match.objects.get(pk=pk)
            serializer = self.serializer_class(match, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse.success(serializer.data, status=200)
            return CustomResponse.error(serializer.errors, status=400)
        except Match.DoesNotExist:
            return CustomResponse.error("Match does not exist", status=404)


class DeleteMatchView(APIView):
    serializer_class = MatchSerializer

    @extend_schema(
        summary="Delete a match",
        description="Delete a match with the specified id.",
    )
    def delete(self, request, pk):
        try:
            match = Match.objects.get(pk=pk)
            match.delete()
            return CustomResponse.success("Match deleted successfully.", status=200)
        except Match.DoesNotExist:
            return CustomResponse.error("Match does not exist", status=404)


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
                    if match.status == Match.MATCH_STATUS_CHOICES.IN_PROGRESS:
                        # Update the match status
                        match.status = Match.MATCH_STATUS_CHOICES.COMPLETED
                        match.save()

                        # Update the players and mediator
                        match.player_1.is_active = False
                        match.player_2.is_active = False
                        match.mediator.is_active = False

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
