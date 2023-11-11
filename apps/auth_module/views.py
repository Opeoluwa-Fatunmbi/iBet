import uuid
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from rest_framework.views import APIView
import asgiref.sync
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle
from apps.core.utils import is_uuid
from apps.betting.models import Match, Bet, Outcome
from apps.core.exceptions import RequestError
from apps.core.responses import CustomResponse
from apps.core.models import File
from apps.core.models import GuestUser
from django.contrib.auth import authenticate, login, logout
from apps.auth_module.models import User, Otp, Jwt
from apps.auth_module.serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    LoginSerializer,
    ResendOtpSerializer,
    RefreshSerializer,
    SetNewPasswordSerializer,
)
from .emails import Util
from rest_framework.exceptions import ValidationError
from apps.auth_module.auth import Authentication
from rest_framework.exceptions import NotFound, AuthenticationFailed


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Register a new user",
        description="This endpoint registers new users into our application",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data

                def check_existing_user(email):
                    existing_user = User.objects.filter(email=email).first()
                    return existing_user

                existing_user = check_existing_user(data["email"])

                if existing_user:
                    response_data = {
                        "status": "Invalid Entry",
                        "message": "Email already registered!",
                    }
                    return CustomResponse.error(response_data, status_code=400)

                # Create user
                user = serializer.save()
                # Send verification email
                Util.send_activation_otp(user)

                response_data = {
                    "status": "success",
                    "message": "Account created successfully. Please check your email for OTP.",
                    "data": {
                        "first_name": data["first_name"],
                        "last_name": data["last_name"],
                        "email": data["email"],
                        "terms_agreement": data["terms_agreement"],
                    },
                }
                return CustomResponse.success(response_data, status_code=400)

        except IntegrityError as e:
            # Handle database integrity error (e.g., unique constraint violation)
            response_data = {
                "status": "failed",
                "message": "Account not created",
                "error_message": str(e),
            }
            return CustomResponse.error(response_data, status_code=400)
        except Exception as e:
            # Handle other exceptions
            response_data = {
                "status": "failed",
                "message": "Account not created",
                "error_message": str(e),
            }
            return CustomResponse.error(response_data, status_code=500)


class LoginView(APIView):
    serializer_class = LoginSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="User Login",
        description="Authenticate and log in a user.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise AuthenticationFailed("Invalid credentials")

            if not user.is_email_verified:
                raise AuthenticationFailed("Verify your email first")

            Jwt.objects.filter(user_id=user.id).delete()

            access = Authentication.create_access_token({"user_id": str(user.id)})
            refresh = Authentication.create_refresh_token()
            Jwt.objects.create(user_id=user.id, access=access, refresh=refresh)

            return CustomResponse.success(
                message="Login successful",
                data={"access": access, "refresh": refresh},
                status_code=201,
            )

        except User.DoesNotExist:
            raise NotFound("User not found")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User Logout",
        description="Log out the currently authenticated user.",
    )
    def post(self, request):
        # Access the user's JWT token from the request (if it exists)
        token = request.auth

        if token:
            # Blacklist the token using Authentication class
            Authentication.blacklist_token(token)

        # Log the user out
        logout(request)

        # Return a response indicating successful logout
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

        user = get_object_or_404(User, email=email)

        if user.is_email_verified:
            return Response(
                {"error": "Email already verified"}, status=status.HTTP_409_CONFLICT
            )

        otp = get_object_or_404(Otp, user=user)

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
                user = User.objects.get(email=email)
            except User.DoesNotExist:
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
                user = User.objects.get(email=email)
            except User.DoesNotExist:
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

            # Use get_object_or_404 for user and OTP retrieval
            user = get_object_or_404(User, email=email)
            otp = get_object_or_404(Otp, user=user)

            if otp.code != code:
                return Response(
                    {"error": "Incorrect OTP"}, status=status.HTTP_401_UNAUTHORIZED
                )

            if otp.check_expiration():
                return Response(
                    {"error": "Expired OTP"}, status=status.HTTP_401_UNAUTHORIZED
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
