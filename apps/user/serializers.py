from rest_framework import serializers
from apps.user.models import User



class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=12, min_length=6, write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ["username","email", "password"]
