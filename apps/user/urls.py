from django.urls import path
from apps.user.views import *


app_name = 'apps.core'


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    #path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('password/change/', PasswordChangeView.as_view(), name='password_change'),

    # Registration URLs
    path('signup/', Signup.as_view(), name='signup'),
    #path('registration/verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    #path('registration/verify-email/confirm/', ConfirmEmailView.as_view(), name='confirm_email'),
]

