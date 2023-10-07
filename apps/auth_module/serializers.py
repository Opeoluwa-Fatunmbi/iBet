from rest_framework import serializers
from apps.auth_module.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUserSerializer handles the serialization of user data.

    It includes fields for user details and role_id.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "role"]

    def create(self, validated_data):
        """
        Create a new user instance and set the password.
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Update the user instance with the provided validated data.
        """
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
