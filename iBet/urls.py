from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



def trigger_error(request):
  division_by_zero = 1 / 0

schema_view = get_schema_view(
    openapi.Info(
        title="iBet API",
        default_version='v1',
        description="iBet",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="opeoluwafatunmbi@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/', include("admin.urls")),
    path('', include('core.urls')), 
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
