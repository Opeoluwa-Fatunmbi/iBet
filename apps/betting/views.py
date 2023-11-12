from rest_framework.views import APIView
from apps.betting.models import Match, Bet, Outcome
from .serializers import CreateMatchSerializer, BetSerializer, OutcomeSerializer
from apps.core.responses import CustomResponse
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema


class CreateMatchView(APIView):
    serializer_class = CreateMatchSerializer
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        summary="Create a new match",
        description="Create a new match with the winner, loser, and mediator.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                winner = serializer.validated_data.get("winner")
                loser = serializer.validated_data.get("loser")
                mediator = serializer.validated_data.get("mediator")

                Match.objects.create(winner=winner, loser=loser, mediator=mediator)


                serializer.save()
                return CustomResponse.success(serializer.data, status=201)

            return CustomResponse.error(serializer.errors, status=400)

        except Exception as e:
            return CustomResponse.error(str(e), status=400)


class BetListCreateView(APIView):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer


class OutcomeListCreateView(APIView):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
