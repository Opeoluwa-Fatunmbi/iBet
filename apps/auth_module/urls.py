from django.urls import path
from apps.auth_module.views import (
    ListUsers,
    CreateUser,
    RetrieveUpdateDeleteUser,
    UserConfirmEmailAddress,
    UserForgetPassword,
    UserResetPassword,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("signup/", CreateUser.as_view(), name="signup"),
    path("users/", ListUsers.as_view(), name="list-users"),
    path(
        "users/<str:pk>/",
        RetrieveUpdateDeleteUser.as_view(),
        name="retrive-update-delete-User",
    ),
    path("sign_in/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh_token/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "confirm_email/", UserConfirmEmailAddress.as_view(), name="confirm-user-email"
    ),
    path("forget_password/", UserForgetPassword.as_view(), name="forget-user-password"),
    path("reset_password/", UserResetPassword.as_view(), name="reset-user-password"),
]
