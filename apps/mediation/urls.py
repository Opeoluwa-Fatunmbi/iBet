from django.urls import path
from apps.mediation.views import MediatorListCreateView, MediationListCreateView

app_name = "apps.mediation"


urlpatterns = [
    path("mediators/", MediatorListCreateView.as_view(), name="mediator-list-create"),
    path(
        "mediations/", MediationListCreateView.as_view(), name="mediation-list-create"
    ),
]
