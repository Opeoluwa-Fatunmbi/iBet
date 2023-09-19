from django.shortcuts import render
from rest_framework.views import APIView
from apps.user.serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework import status



class Signup(APIView):

    serializer_class = SignupSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


