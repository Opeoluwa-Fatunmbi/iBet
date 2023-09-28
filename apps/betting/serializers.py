from rest_framework import serializers
from apps.betting.models import Match, Bet, Outcome


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = "__all__"


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = "__all__"
