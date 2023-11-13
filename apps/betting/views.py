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
        description="Create a new match with the player_1, player_2, and mediator.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                player_1 = serializer.validated_data.get("player_1")
                player_2 = serializer.validated_data.get("player_2")
                mediator = serializer.validated_data.get("mediator")

                Match.objects.create(
                    player_1=player_1, player_2=player_2, mediator=mediator
                )

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
