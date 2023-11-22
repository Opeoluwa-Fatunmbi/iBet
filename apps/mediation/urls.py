from django.urls import path
from apps.mediation.views import (
    MediatorList,
    MediatorDetail,
    DeleteMediator,
    CreateMediator,
    MediationDetail,
    MediationList,
    CreateMediation,
    DeleteMediation,
    UpdateMediation,
)

app_name = "apps.mediation"


urlpatterns = [
    path("mediators/", MediatorList.as_view(), name="mediator-list"),
    path("mediators/create/", CreateMediator.as_view(), name="mediator-create"),
    path(
        "mediators/<uuid:pk>/detail/", MediatorDetail.as_view(), name="mediator-detail"
    ),
    path(
        "mediators/<uuid:pk>/delete/", DeleteMediator.as_view(), name="mediator-delete"
    ),
    path("mediations/", MediationList.as_view(), name="mediation-list"),
    path("mediations/create/", CreateMediation.as_view(), name="mediation-create"),
    path(
        "mediations/<uuid:pk>/detail/",
        MediationDetail.as_view(),
        name="mediation-detail",
    ),
    path(
        "mediations/<uuid:pk>/delete/",
        DeleteMediation.as_view(),
        name="mediation-delete",
    ),
    path(
        "mediations/<uuid:pk>/update/",
        UpdateMediation.as_view(),
        name="mediation-update",
    ),
]
