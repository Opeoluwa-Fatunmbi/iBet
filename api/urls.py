from django.urls import path
from .views import (
    Signup,
    Login,
    Logout,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('user/signup/', Signup.as_view(), name='user_signup'),
    path('user/login/', Login.as_view(), name='user_login'),
    path('user/logout/', Logout.as_view(), name='user_logout'),

    #TOKEN
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
