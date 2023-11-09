from rest_framework import serializers
from apps.betting.models import Match, Bet, Outcome


class MatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    winner = serializers.CharField(max_length=100)
    loser = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = "__all__"


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = "__all__"
