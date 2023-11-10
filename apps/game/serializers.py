# serializers.py
from rest_framework import serializers
from apps.auth_module.models import User
from .models import Game, Player
from apps.auth_module.serializers import UserSerializer


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    rules = serializers.CharField(max_length=500)
    game = serializers.ChoiceField(
        choices=Game.Games.choices, default=Game.Games.EIGHTBALL
    )
    goal = serializers.CharField(max_length=200)
    min_players = serializers.IntegerField(default=2)
    max_players = serializers.IntegerField(default=2)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.rules = validated_data.get("rules", instance.rules)
        instance.game = validated_data.get("game", instance.game)
        instance.goal = validated_data.get("goal", instance.goal)
        instance.min_players = validated_data.get("min_players", instance.min_players)
        instance.max_players = validated_data.get("max_players", instance.max_players)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class PlayerSerializer(serializers.Serializer):
    user = UserSerializer()
    score = serializers.IntegerField(default=0)
    experience_level = serializers.CharField(
        max_length=50, allow_blank=True, allow_null=True
    )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        return Player.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.score = validated_data.get("score", instance.score)
        instance.experience_level = validated_data.get(
            "experience_level", instance.experience_level
        )
        instance.save()
        return instance
