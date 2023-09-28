from rest_framework import generics
from .models import Mediator, Mediation
from .serializers import MediatorSerializer, MediationSerializer


class MediatorListCreateView(generics.ListCreateAPIView):
    queryset = Mediator.objects.all()
    serializer_class = MediatorSerializer


class MediationListCreateView(generics.ListCreateAPIView):
    queryset = Mediation.objects.all()
    serializer_class = MediationSerializer
