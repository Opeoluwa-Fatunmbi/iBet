from django.urls import path
from apps.betting.views import (
    MatchListCreateView,
    BetListCreateView,
    OutcomeListCreateView,
)

app_name = "apps.betting"

urlpatterns = [
    path("matches/", MatchListCreateView.as_view(), name="match-list-create"),
    path("bets/", BetListCreateView.as_view(), name="bet-list-create"),
    path("outcomes/", OutcomeListCreateView.as_view(), name="outcome-list-create"),
]
