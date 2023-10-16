from django.urls import path
from apps.auth_module.views import (
    ListUsers,
    LoginView,
    LogoutView,
    SignupView,
    RetrieveUser,
    UserConfirmEmailAddress,
    UserForgetPassword,
    UserResetPassword,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", ListUsers.as_view(), name="list-users"),
    path(
        "user/<str:pk>/",
        RetrieveUser.as_view(),
        name="retrieve-user",
    ),
    # path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh_token/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "confirm_email/", UserConfirmEmailAddress.as_view(), name="confirm-user-email"
    ),
    path("forget_password/", UserForgetPassword.as_view(), name="forget-user-password"),
    path("reset_password/", UserResetPassword.as_view(), name="reset-user-password"),
]
