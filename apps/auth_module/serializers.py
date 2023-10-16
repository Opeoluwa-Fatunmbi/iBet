from rest_framework import serializers
from apps.auth_module.models import CustomUser
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8, error_messages={"min_length": _("{min_length} characters min.")}
    )
    terms_agreement = serializers.BooleanField()

    def validate(self, attrs):
        email = attrs["email"]
        terms_agreement = attrs["terms_agreement"]

        if len(email.split(" ")) > 1:
            raise serializers.ValidationError({"email": "No spacing allowed"})

        if terms_agreement != True:
            raise serializers.ValidationError(
                {"terms_agreement": "You must agree to terms and conditions"}
            )
        return attrs



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    password = serializers.CharField(
        min_length=8, error_messages={"min_length": _("{min_length} characters min.")}
    )

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()