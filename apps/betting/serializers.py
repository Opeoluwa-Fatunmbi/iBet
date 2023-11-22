from rest_framework import serializers
from apps.betting.models import Match, Bet, Outcome
from apps.game.models import Game
from apps.auth_module.serializers import UserSerializer
from apps.auth_module.models import User


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

    def create(self, validated_data):
        user = self.context["request"].user
        amount = validated_data["amount"]

        # Deduct amount from the user's wallet
        user_wallet = user.wallet
        user_wallet.balance -= amount
        user_wallet.save()

        # Create the bet
        bet = Bet.objects.create(player=user.player, **validated_data)

        # Set is_active to True
        bet.is_active = True
        bet.save()

        return bet


class OutcomeSerializer(serializers.Serializer):
    match = serializers.CharField(max_length=100)
    winner = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Outcome.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.match = validated_data.get("match", instance.match)
        instance.winner = validated_data.get("winner", instance.winner)
        instance.save()
        return instance

    def validate_match(self, value):
        if not Match.objects.filter(id=value).exists():
            raise serializers.ValidationError("Match does not exist")
        return value

    def validate_winner(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value

    def to_representation(self, instance):
        self.fields["match"] = MatchSerializer(read_only=True)
        return super(OutcomeSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields["match"] = serializers.PrimaryKeyRelatedField(
            queryset=Match.objects.all()
        )
        return super(OutcomeSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        match = validated_data["match"]
        winner = validated_data["winner"]

        # Set the match status to completed
        match.status = Match.MATCH_STATUS_CHOICES.COMPLETED
        match.save()

        # Set the match winner
        match.winner = winner
        match.save()

        # Set the bet status to completed
        bets = Bet.objects.filter(match=match)
        for bet in bets:
            bet.is_active = False
            bet.save()

        # Add the amount to the winner's wallet
        winner_wallet = winner.wallet
        winner_wallet.balance += match.amount
        winner_wallet.save()

        return Outcome.objects.create(**validated_data)


class MatchSerializer(serializers.Serializer):
    player_1 = serializers.CharField(max_length=100)
    player_2 = serializers.CharField(max_length=100)
    mediator = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    game = serializers.ChoiceField(choices=Game.Games.choices)

    def create(self, validated_data):
        return Match.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.player_1 = validated_data.get("player_1", instance.player_1)
        instance.player_2 = validated_data.get("player_2", instance.player_2)
        instance.mediator = validated_data.get("mediator", instance.mediator)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.game = validated_data.get("game", instance.game)
        instance.save()
        return instance
