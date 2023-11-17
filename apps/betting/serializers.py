from rest_framework import serializers
from apps.betting.models import Match, Bet, Outcome


class CreateMatchSerializer(serializers.Serializer):
    player_1 = serializers.CharField(max_length=100)
    player_2 = serializers.CharField(max_length=100)
    mediator = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)


class MatchSerializer(serializers.Serializer):
    player_1 = serializers.CharField(max_length=100)
    player_2 = serializers.CharField(max_length=100)
    mediator = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)


class BetSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    game = serializers.CharField(max_length=100)


class OutcomeSerializer(serializers.Serializer):
    winner = serializers.CharField(max_length=100)
    loser = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Outcome.objects.create(**validated_data)
