from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    #VerifyEmailView,
    #ResendEmailVerificationView,
)

app_name = 'core'

urlpatterns = [
    # dj-rest-auth URLs
    path('rest-auth/login/', LoginView.as_view(), name='rest_login'),
    path('rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('rest-auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('rest-auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('rest-auth/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    #path('rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
    #path('rest-auth/registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    #path('rest-auth/registration/resend-verification-email/', ResendEmailVerificationView.as_view(), name='rest_resend_verification_email'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
