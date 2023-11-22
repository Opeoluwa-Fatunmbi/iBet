from django.urls import path
from apps.betting.views import (
    MatchDetailView,
    MatchListView,
    BetDetailView,
    ConfirmOutcomeView,
    BetListView,
    CreateBetView,
    ListOutcomesView,
    OutcomeDetailView,
    DeleteBetView,
    DeleteOutcomeView,
    UpdateOutcomeView,
    DeleteMatchView,
)

app_name = "apps.betting"

urlpatterns = [
    path("bets/", BetListView.as_view(), name="bet-list"),
    path("matches/", MatchListView.as_view(), name="match-list"),
    path("matches/<uuid:pk>/detail/", MatchDetailView.as_view(), name="match-detail"),
    path("bets/create/", CreateBetView.as_view(), name="bet-create"),
    path("bets/<uuid:pk>/detail/", BetDetailView.as_view(), name="bet-detail"),
    path("bets/<uuid:pk>/delete/", DeleteBetView.as_view(), name="bet-delete"),
    path("matches/<uuid:pk>/delete/", DeleteMatchView.as_view(), name="match-delete"),
    path("outcomes/", ListOutcomesView.as_view(), name="outcome-list"),
    path(
        "outcomes/<uuid:pk>/detail/", OutcomeDetailView.as_view(), name="outcome-detail"
    ),
    path(
        "outcomes/<uuid:pk>/delete/", DeleteOutcomeView.as_view(), name="outcome-delete"
    ),
    path(
        "outcomes/<uuid:pk>/update/", UpdateOutcomeView.as_view(), name="outcome-update"
    ),
    path(
        "bets/<uuid:pk>/confirm-outcome/",
        ConfirmOutcomeView.as_view(),
        name="confirm-outcome",
    ),
]
