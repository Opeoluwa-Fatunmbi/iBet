from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from apps.auth_module.models import CustomUser
from apps.auth_module.serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import uuid


class CreateUsers(APIView):
    """
    CreateUsers class handles the creation of user accounts.

    POST: Create a new user account and send a confirmation email(requires admin authentication)..
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        """
        POST method to create a new user account and send a confirmation email(requires admin authentication)..
        """
        data = request.data
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            # Send a confirmation email with a confirmation link
            subject = "Confirm your email address"
            message = "Click the link to confirm your email address"
            from_email = "abiolaadedayo1993@gmail.com"
            recipient_list = [user.email]

            # Generate a confirmation URL

            confirmation_url = f"http://127.0.0.1:8000/api/v1/confirm_email?user_id={user.id}&token={user.confirm_email_token}"

            message += f"\n\n{confirmation_url}"

            send_mail(subject, message, from_email, recipient_list)
            response = {
                "status": "success",
                "message": "Account created successfully. Please check your email for a confirmation link.",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        bad_request_response = {
            "status": "failed",
            "message": "Account not created",
            "error_message": serializer.errors,
        }
        return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)


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


class RetrieveUpdateDeleteUser(APIView):
    """
    RetrieveUpdateDeleteUser class handles the retrieval, update, and deletion of user accounts.

    GET: Retrieve detailed information about a specific user account.
    PUT: Update user account information (allows partial updates).
    DELETE: Delete a specific user account.
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

    def put(self, request: Request, pk):
        """
        PUT method to update user account information (allows partial updates).
        """
        try:
            queryset = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            error_response = {"status": "error", "message": "User not found"}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user.email != queryset.email:
            authentication_response = {
                "status": "failed",
                "message": "User Not Authorized",
            }
            return Response(authentication_response, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = CustomUserSerializer(queryset, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Account updated suucessfully",
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        bad_request_response = {
            "status": "failed",
            "message": "Account update failed",
            "error_message": serializer.errors,
        }
        return Response(bad_request_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk):
        try:
            queryset = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            error_response = {"status": "error", "message": "User not found"}
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.email != queryset.email:
            authentication_response = {
                "status": "failed",
                "message": "User Not Authorized",
            }
            return Response(authentication_response, status=status.HTTP_403_FORBIDDEN)
        queryset.delete()
        response = {"status": "success", "message": "Account deleted successfully."}
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
        user_id = request.query_params.get("user_id")
        confirm_email_token = request.query_params.get("token")

        try:
            user = CustomUser.objects.get(pk=user_id)
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

        forget_password_url = f"http://127.0.0.1:8000/api/v1/reset_password?user_id={user.id}&token={user.reset_password_token}/"

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
