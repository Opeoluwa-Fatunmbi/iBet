import uuid
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from adrf.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import authenticate, login, logout
from apps.auth_module.models import CustomUser
from apps.auth_module.serializers import RegisterSerializer
from .emails import Util
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync


class SignupView(APIView):
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

                # Check for existing user by email
                existing_user = CustomUser.objects.filter(email=data["email"]).first()

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


class ListUsers(APIView):
    """
    ListUsers class handles the listing of user accounts.

    GET: List all user accounts (requires admin authentication).
    """

    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        """
        GET method to list all user accounts (requires admin authentication).
        """
        queryset = CustomUser.objects.all()
        serializer = CustomUserSerializer(instance=queryset, many=True)
        response = {"status": "success", "data": serializer.data}
        return Response(response, status=status.HTTP_200_OK)


class RetrieveUser(APIView):
    """
    GET: Retrieve detailed information about a specific user account.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        """
        GET method to retrieve detailed information about a specific user account by using its id.
        """
        try:
            queryset = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            error_response = {"status": "error", "message": "User not found"}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(instance=queryset)
        user = request.user
        if user.email != queryset.email:
            authentication_response = {
                "status": "failed",
                "message": "User Not Authorized",
            }
            return Response(authentication_response, status=status.HTTP_403_FORBIDDEN)
        response = {"status": "success", "data": serializer.data}
        return Response(response, status=status.HTTP_200_OK)


class UserConfirmEmailAddress(APIView):
    """
    UserConfirmEmailAddress class handles the confirmation of a user's email address.

    GET: Confirm a user's email address with a valid token.
    """

    permission_classes = [AllowAny]

    def get(self, request: Request):
        """
        GET method to confirm a user's email address with a valid token.
        """
        user_id = request.query_params.get("id")
        confirm_email_token = request.query_params.get("token")

        try:
            user = CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            error_response = {"status": "error", "message": "User not found"}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        if user_id != str(user.pk) or confirm_email_token != str(
            user.confirm_email_token
        ):
            authentication_response = {
                "status": "failed",
                "message": "User Not Authorized",
            }
            return Response(authentication_response, status=status.HTTP_403_FORBIDDEN)

        if confirm_email_token == str(user.confirm_email_token):
            user.confirm_email_token = None
            user.save()
            response = {"status": "success", "Message": "User Account email confirmed"}
            return Response(response, status=status.HTTP_200_OK)
        error_response = {"status": "failed", "message": "Invalid Token"}
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


class UserForgetPassword(APIView):
    """
    UserForgetPassword class handles the initiation of the forget password process.

    GET: Initiate the forget password process by sending an email with a reset password link.
    """

    permission_classes = [AllowAny]

    def get(self, request: Request):
        """
        GET method to initiate the forget password process by sending an email with a reset password link.
        """
        email = request.query_params.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            error_response = {"status": "error", "message": "User not found"}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        # Send a confirmation email with a forget password link
        subject = "Reset your password"
        message = "Click the link to reset your password"
        from_email = "abiolaadedayo1993@gmail.com"
        recipient_list = [email]

        # Generate a forget password URL

        forget_password_url = f"http://127.0.0.1:8000/api/v1/reset_password?id={user.id}&token={user.reset_password_token}/"

        message += f"\n\n{forget_password_url}"

        try:
            send_mail(subject, message, from_email, recipient_list)
            response = {"status": "success", "message": "Email sent successfully"}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            failed_response = {
                "status": "failed",
                "message": f"Email not sent: {str(e)}",
            }
            return Response(failed_response, status=status.HTTP_400_BAD_REQUEST)


class UserResetPassword(APIView):
    """
    UserResetPassword class handles the reset of a user's password.

    PUT: Reset a user's password with a valid token.
    """

    permission_classes = [AllowAny]

    def put(self, request: Request):
        """
        PUT method to reset a user's password with a valid token.
        """
        user_id = request.query_params.get("user_id")
        reset_password_token = request.query_params.get("token")

        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            error_response = {"status": "error", "message": "User not found"}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        if user_id != str(user.id) or reset_password_token != str(
            user.reset_password_token
        ):
            authentication_response = {
                "status": "failed",
                "message": "User Not Authorized",
            }
            return Response(authentication_response, status=status.HTTP_403_FORBIDDEN)

        if reset_password_token == str(user.reset_password_token):
            user.reset_password_token = uuid.uuid4()
            data = request.data
            serializer = CustomUserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "status": "success",
                    "message": "Password reset successfully",
                }
                return Response(response, status=status.HTTP_202_ACCEPTED)
        bad_request_response = {
            "status": "failed",
            "message": "Account update failed",
            "error_message": serializer.errors,
        }
        return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)
