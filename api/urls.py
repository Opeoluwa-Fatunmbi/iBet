from django.urls import path
from .views import (
    UserCreate,
    Login,
    #AddInfo,
    #UpdateInfo,
    #ForgotPassword,
    Logout,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('user/create/', UserCreate.as_view(), name='user_create'),
    path('user/login/', Login.as_view(), name='user_login'),
    #path('user/addinfo/', AddInfo.as_view(), name='user_addinfo'),
    #path('user/updateinfo/', UpdateInfo.as_view(), name='user_updateinfo'),
    # path('user/updatephoto/', UpdatePhoto.as_view(), name='update_photo'),
    #path('user/forgotpassword/', ForgotPassword.as_view(), name='forgot_password'),
    path('user/logout/', Logout.as_view(), name='user_logout'),
    #path('user/createcontact/', CreateContact.as_view(), name='create_contact'),
    #path('user/updatecontact/', UpdateContact.as_view(), name='update_contact'),
    
    #path('addnewcard/', AddNewCard.as_view(), name='add_new_card'),



    #TOKEN
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
