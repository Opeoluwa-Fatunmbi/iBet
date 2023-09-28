from rest_framework import serializers
from .models import Mediator, Mediation


class MediatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mediator
        fields = "__all__"


class MediationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mediation
        fields = "__all__"
