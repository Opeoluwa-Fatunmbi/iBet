# serializers.py
from rest_framework import serializers
from apps.auth_module.models import User
from apps.game.models import Game, Player
from apps.auth_module.serializers import UserSerializer


class GameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    rules = serializers.CharField(max_length=500)
    game = serializers.ChoiceField(
        choices=Game.Games.choices, default=Game.Games.EIGHTBALL
    )
    goal = serializers.CharField(max_length=200)
    is_active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.rules = validated_data.get("rules", instance.rules)
        instance.game = validated_data.get("game", instance.game)
        instance.goal = validated_data.get("goal", instance.goal)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class PlayerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    experience_level = serializers.CharField(
        max_length=50, default=Player.ExperienceLevel.BEGINNER
    )

    def create(self, validated_data):
        return Player.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.experience_level = validated_data.get(
            "experience_level", instance.experience_level
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(PlayerSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields["user"] = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all()
        )
        return super(PlayerSerializer, self).to_internal_value(data)
