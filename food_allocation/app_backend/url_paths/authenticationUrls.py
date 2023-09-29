from django.urls import path
from app_backend.views import authenticationViews

urlpatterns = [
    path("register", authenticationViews.authenticationRegister, name="register"),
    path("login", authenticationViews.authenticationLogin, name="login"),
    path("logout", authenticationViews.authenticationLogout, name="logout"),
    path("profile", authenticationViews.authenticationDisplayProfile, name="profile"),
]
