from django.urls import path
from apps.betting.views import (
    MatchDetailView,
    MatchListView,
    BetDetailView,
    ConfirmOutcomeView,
    BetListView,
    CreateBetView,
    # OutcomeView,
)

app_name = "apps.betting"

urlpatterns = [
    path("bets/", BetListView.as_view(), name="bet-list"),
    path("matches/", MatchListView.as_view(), name="match-list"),
    path("matches/<uuid:pk>/detail/", MatchDetailView.as_view(), name="match-detail"),
    path("bets/create/", CreateBetView.as_view(), name="bet-create"),
    path("bets/<uuid:pk>/detail/", BetDetailView.as_view(), name="bet-detail"),
    path(
        "bets/<uuid:pk>/confirm-outcome/",
        ConfirmOutcomeView.as_view(),
        name="confirm-outcome",
    ),
    # path("outcomes/", OutcomeView.as_view(), name="outcome"),
]
