from django.urls import path

from .api.v1.logout_user_view import LogoutUserView
from .api.v1.register_user_view import RegisterUserView
from rest_framework.authtoken import views as drf_authtoken

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register_user"),
    path("logout/", LogoutUserView.as_view(), name="logout_user"),
    path("token/", drf_authtoken.obtain_auth_token, name="obtain_auth_token"),
]
