from rest_framework.views import APIView
from apps.betting.models import Match, Bet, Outcome
from .serializers import (
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
    permission_classes = [IsAuthenticated, IsPlayer]

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
    throttle_classes = [UserRateThrottle]

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
    throttle_classes = [UserRateThrottle]

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
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Confirm outcome",
        description="Confirm the outcome of a match.",
    )
    def post(self, request, pk):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        try:
            if serializer.is_valid(raise_exception=True):
                match = Match.objects.get(pk=pk)
                winner = serializer.validated_data["winner"]

                # Check if the match is active
                if match.is_active:
                    # Check if the winner is one of the players
                    if (
                        match.player_1.user.username == winner
                        or match.player_2.user.username == winner
                    ):
                        # Update the match status to completed
                        match.MATCH_STATUS_CHOICES = "COMPLETED"
                        match.save()

                        # Update the winner's wallet balance
                        winner_wallet = match.winner.wallet
                        winner_wallet.balance += match.amount
                        winner_wallet.save()

                        # Update the loser's wallet balance
                        loser = (
                            match.player_1.user.username
                            if match.player_2.user.username == winner
                            else match.player_2.user.username
                        )
                        loser_wallet = match.loser.wallet
                        loser_wallet.balance -= match.amount
                        loser_wallet.save()

                        # Update the players and mediator to be available
                        match.player_1.is_active = False
                        match.player_2.is_active = False
                        match.mediator.is_active = False
                        match.player_1.save()
                        match.player_2.save()
                        match.mediator.save()

                        # Create the outcome
                        serializer.save(match=match)

                        return CustomResponse.success(serializer.data, status=201)
                    else:
                        return CustomResponse.error(
                            {"error": "Winner is not one of the players."}, status=400
                        )
                else:
                    return CustomResponse.error(
                        {"error": "Match is not active."}, status=400
                    )

            return CustomResponse.error(serializer.errors, status=400)
        except Exception as e:
            return CustomResponse.error({"error": str(e)}, status=500)


class ListOutcomesView(APIView):
    serializer_class = OutcomeSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="List outcomes",
        description="List all outcomes.",
    )
    def get(self, request):
        outcomes = Outcome.objects.all()
        serializer = self.serializer_class(outcomes, many=True)
        if serializer.is_valid(raise_exception=True):
            return CustomResponse.success(serializer.data, status=200)
        return CustomResponse.error(serializer.errors, status=404)


class OutcomeDetailView(APIView):
    serializer_class = OutcomeSerializer

    @extend_schema(
        summary="Get an outcome",
        description="Get an outcome with the match, winner, and loser.",
    )
    def get(self, request, pk):
        try:
            outcome = Outcome.objects.get(pk=pk)
            serializer = self.serializer_class(outcome)
            return CustomResponse.success(serializer.data, status=200)

        except Outcome.DoesNotExist:
            return CustomResponse.error("Outcome does not exist", status=404)


class UpdateOutcomeView(APIView):
    serializer_class = OutcomeSerializer

    @extend_schema(
        summary="Update an outcome",
        description="Update an outcome with the specified id.",
    )
    def put(self, request, pk):
        try:
            outcome = Outcome.objects.get(pk=pk)
            serializer = self.serializer_class(outcome, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return CustomResponse.success(serializer.data, status=200)
            return CustomResponse.error(serializer.errors, status=400)
        except Outcome.DoesNotExist:
            return CustomResponse.error("Outcome does not exist", status=404)


class DeleteOutcomeView(APIView):
    serializer_class = OutcomeSerializer

    @extend_schema(
        summary="Delete an outcome",
        description="Delete an outcome with the specified id.",
    )
    def delete(self, request, pk):
        try:
            outcome = Outcome.objects.get(pk=pk)
            outcome.delete()
            return CustomResponse.success("Outcome deleted successfully.", status=200)
        except Outcome.DoesNotExist:
            return CustomResponse.error("Outcome does not exist", status=404)
