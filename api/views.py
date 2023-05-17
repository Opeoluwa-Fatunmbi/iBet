from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    User,
    Game, 
    Transaction,
    UserContact
)
from .serializers import (
    UserSerializer,
)



#-----------------------------------------------------------#


# ------Create user------#
class Signup(APIView):
    #-------Authentication-----#
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                #------Login User------#
                login(request, user)
                #------create tokens for the user------#
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                #------serialize the response------#
                data = {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
  

                return Response(data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'User with this email or username already exists.'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------Log user in------#
class Login(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # ------create tokens for the user------#
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # ------serialize the response------#
            data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )



# ------Log user out------#
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = self.get_serializer().validate(request.data['token'])
        self.token_blacklist.add(token)
        logout(request)
        return Response(status=status.HTTP_200_OK)
