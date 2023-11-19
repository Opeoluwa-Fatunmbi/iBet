from rest_framework import serializers
from apps.betting.models import Match, Bet, Outcome
from apps.game.models import Game
from apps.auth_module.serializers import UserSerializer
from iBet.apps.auth_module.models import User


class BetSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    game = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Bet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.game = validated_data.get("game", instance.game)
        instance.save()
        return instance

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value

    def validate_game(self, value):
        if value not in Game.Games.values:
            raise serializers.ValidationError("Game is not valid")
        return value

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(BetSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields["user"] = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all()
        )
        return super(BetSerializer, self).to_internal_value(data)


class OutcomeSerializer(serializers.Serializer):
    pass


"""
class CreateMatchSerializer(serializers.Serializer):
    player_1 = serializers.CharField(max_length=100)
    player_2 = serializers.CharField(max_length=100)
    mediator = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    game = serializers.ChoiceField(choices=Game.Games.choices)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)


class FindMatchSerializer(serializers.Serializer):
    player_1 = serializers.CharField(max_length=100)
    player_2 = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    game = serializers.ChoiceField(choices=Game.Games.choices)


class MatchSerializer(serializers.Serializer):
    player_1 = serializers.CharField(max_length=100)
    player_2 = serializers.CharField(max_length=100)
    mediator = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)
"""
