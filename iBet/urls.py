from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('admin/defender/', include('defender.urls')), # defender admin
    # Apps
    path("api/v1/auth/", include("apps.auth_module.urls")),
    path("api/v1/betting/", include("apps.betting.urls")),
    path("api/v1/game/", include("apps.game.urls")),
    path("api/v1/mediation/", include("apps.mediation.urls")),
    path("api/v1/billing/", include("apps.billing.urls")),
    # Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Debug Toolbar
    path("__debug__/", include(debug_toolbar.urls)),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
