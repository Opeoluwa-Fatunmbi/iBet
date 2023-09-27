from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings


def trigger_error(request):
    division_by_zero = 1 / 0


schema_view = get_schema_view(
    openapi.Info(
        title="iBet API",
        default_version="v1",
        description="iBet",
        terms_of_service="https://www.iBet.com/terms/",
        contact=openapi.Contact(email="opeoluwafatunmbi@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/v1/core', include('core.urls')),
    path("api/v1/auth/", include("apps.auth_module.urls")),
    path("api/v1/betting/", include("apps.betting.urls")),
    path("api/v1/game/", include("apps.game.urls")),
    path("api/v1/mediation/", include("apps.mediation.urls")),
    path("api/v1/billing/", include("apps.billing.urls")),
    # Documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
