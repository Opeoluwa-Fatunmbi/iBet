from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ConfirmEmailView,
)

app_name = 'core'

urlpatterns = [
    # dj-rest-auth URLs
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),

    # Registration URLs
    path('registration/', RegisterView.as_view(), name='register'),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('registration/verify-email/confirm/', ConfirmEmailView.as_view(), name='confirm_email'),

    # jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
