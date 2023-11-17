from rest_framework import serializers
from .models import Mediator, Mediation
from apps.auth_module.serializers import UserSerializer


class MediatorSerializer(serializers.Serializer):
    is_engaged = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Mediator.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_engaged = validated_data.get("is_engaged", instance.is_engaged)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        self.fields["user"] = UserSerializer(read_only=True)
        return super(MediatorSerializer, self).to_representation(instance)


class MediationSerializer(serializers.Serializer):
    mediator = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=100)
    mediation_results = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Mediation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.mediation_results = validated_data.get(
            "mediation_results", instance.mediation_results
        )
        instance.save()
        return instance
