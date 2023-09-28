from rest_framework import generics
from apps.betting.models import Match, Bet, Outcome
from .serializers import MatchSerializer, BetSerializer, OutcomeSerializer


class MatchListCreateView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class BetListCreateView(generics.ListCreateAPIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer


class OutcomeListCreateView(generics.ListCreateAPIView):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
