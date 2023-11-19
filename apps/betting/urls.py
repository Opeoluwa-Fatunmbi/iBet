from django.urls import path
from apps.betting.views import (
    # MatchView,
    # MatchDetailView,
    # MatchListView,
    BetCreateView,
    BetListView,
    BetDetailView,
    OutcomeView,
    ConfirmOutcomeView,
)

app_name = "apps.betting"

urlpatterns = [
    path("bets/create/", BetCreateView.as_view(), name="bet-create"),
    path("bets/list/", BetListView.as_view(), name="bet-list"),
    path("bets/<uuid:pk>/detail/", BetDetailView.as_view(), name="bet-detail"),
    path(
        "bets/<uuid:pk>/confirm-outcome/",
        ConfirmOutcomeView.as_view(),
        name="confirm-outcome",
    ),
    path("outcomes/", OutcomeView.as_view(), name="outcome"),
]
