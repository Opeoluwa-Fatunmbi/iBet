from rest_framework import serializers
from apps.betting.models import Match, Bet, Outcome
from django.contrib.auth.models import User



class MatchSerializer(serializers.Serializer):
    match_date = serializers.DateTimeField()
    game_type = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=20)
    winner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    loser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    duration_minutes = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False)

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
