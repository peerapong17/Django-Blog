
from django.urls import path
from .views import register_user, login_user,logout_user

urlpatterns = [
    path("register", register_user, name='registerUser'),
    path("login", login_user, name='loginUser'),
    path("logout", logout_user, name='logoutUser'),
]
