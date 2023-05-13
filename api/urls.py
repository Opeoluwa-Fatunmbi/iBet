from django.urls import path
from .views import (
    Signup,
    Login,
    #ForgotPassword,
    Logout,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('user/signup/', Signup.as_view(), name='user_signup'),
    path('user/login/', Login.as_view(), name='user_login'),
    # path('user/updatephoto/', UpdatePhoto.as_view(), name='update_photo'),
    #path('user/forgotpassword/', ForgotPassword.as_view(), name='forgot_password'),
    path('user/logout/', Logout.as_view(), name='user_logout'),
    #path('user/createcontact/', CreateContact.as_view(), name='create_contact'),



    #TOKEN
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
