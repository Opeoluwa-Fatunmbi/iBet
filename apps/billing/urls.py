from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from views import *

app_name = 'apps.billing'

urlpatterns = [
    #path('login/', LoginView.as_view(), name='login'),
]
