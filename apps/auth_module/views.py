import uuid
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from adrf.views import APIView
import asgiref.sync
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate, login, logout
from apps.auth_module.models import CustomUser, Otp, Jwt
from apps.auth_module.serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    ResendOtpSerializer,
    RefreshSerializer,
    SetNewPasswordSerializer,
)
from .emails import Util
from rest_framework.exceptions import ValidationError
from apps.auth_module.auth import Authentication


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Register a new user",
        description="This endpoint registers new users into our application",
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data

                async def check_existing_user(email):
                    existing_user = await CustomUser.objects.filter(email=email).first()
                    return existing_user

                # Call the asynchronous function directly
                existing_user = await check_existing_user(data["email"])

                if existing_user:
                    response_data = {
                        "status": "Invalid Entry",
                        "message": "Email already registered!",
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                # Create user
                user = serializer.save()
                # Send verification email
                await Util.send_activation_otp(user)

                response_data = {
                    "status": "success",
                    "message": "Account created successfully. Please check your email for a confirmation link.",
                    "data": serializer.data,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            # Handle database integrity error (e.g., unique constraint violation)
            response_data = {
                "status": "failed",
                "message": "Account not created",
                "error_message": str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other exceptions
            response_data = {
                "status": "failed",
                "message": "Account not created",
                "error_message": str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    @extend_schema(
        summary="User Login",
        description="Authenticate and log in a user.",
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                data={"status": "success", "message": "User logged in successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"status": "error", "message": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User Logout",
        description="Log out the currently authenticated user.",
    )
    def post(self, request):
        logout(request)
        return Response(
            data={"status": "success", "message": "User logged out successfully."},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(APIView):
    serializer_class = VerifyOtpSerializer

    @extend_schema(
        summary="Verify a user's email",
        description="This endpoint verifies a user's email",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user.is_email_verified:
            return Response(
                {"error": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            otp = Otp.objects.get(user=user)
        except Otp.DoesNotExist:
            return Response(
                {"error": "OTP not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if otp.code != otp_code:
            return Response(
                {"error": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        if otp.check_expiration():
            return Response(
                {"error": "Expired OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.is_email_verified = True
        user.save()
        otp.delete()

        # Send welcome email
        Util.welcome_email(user)

        return Response(
            {"message": "Account verification successful"}, status=status.HTTP_200_OK
        )


class ResendVerificationEmailView(APIView):
    serializer_class = ResendOtpSerializer

    @extend_schema(
        summary="Resend Verification Email",
        description="This endpoint resends a new OTP to the user's email",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if user.is_email_verified:
                return Response(
                    {"error": "Email already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Send verification email
            Util.send_activation_otp(user)
            return Response(
                {"message": "Verification email sent"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetOtpView(APIView):
    serializer_class = ResendOtpSerializer

    @extend_schema(
        summary="Send Password Reset OTP",
        description="This endpoint sends a new password reset OTP to the user's email",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Send password reset email
            Util.send_password_change_otp(user)
            return Response(
                {"message": "Password reset OTP sent"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    @extend_schema(
        summary="Set New Password",
        description="This endpoint verifies the password reset OTP",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data["email"]
            code = data["otp"]
            password = data["password"]

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

            try:
                otp = Otp.objects.get(user=user)
            except Otp.DoesNotExist:
                return Response(
                    {"error": "OTP not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if otp.code != code:
                return Response(
                    {"error": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST
                )

            if otp.check_expiration():
                return Response(
                    {"error": "Expired OTP"}, status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.save()
            otp.delete()

            return Response(
                {"message": "Password reset successful"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokensView(APIView):
    serializer_class = RefreshSerializer

    @extend_schema(
        summary="Refresh tokens",
        description="This endpoint refresh tokens by generating new access and refresh tokens for a user",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        token = data["refresh"]
        jwt = Jwt.objects.filter(refresh=token).first()

        if not jwt:
            return Response(
                {"error": "Refresh token does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        decoded_jwt = Authentication.decode_jwt(token)
        if not decoded_jwt:
            return Response(
                {"error": "Refresh token is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access = Authentication.create_access_token({"user_id": str(jwt.user_id)})
        refresh = Authentication.create_refresh_token()

        jwt.access = access
        jwt.refresh = refresh
        jwt.save()

        response_data = {"access": access, "refresh": refresh}

        return Response(response_data, status=status.HTTP_200_OK)
