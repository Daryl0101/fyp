from django.urls import path
from app_backend.views import authenticationViews

urlpatterns = [
    path("register", authenticationViews.authenticationRegister, name="register"),
    path("login", authenticationViews.authenticationLogin, name="login"),
    path("logout", authenticationViews.authenticationLogout, name="logout"),
    path("profile", authenticationViews.authenticationDisplayProfile, name="profile"),
    path("search", authenticationViews.authenticationSearchUser, name="search"),
    path(
        "details/<uuid:user_id>",
        authenticationViews.authenticationUserDetails,
        name="details",
    ),
    path(
        "update/<uuid:user_id>",
        authenticationViews.authenticationUpdateUser,
        name="update",
    ),
    path(
        "delete/<uuid:user_id>",
        authenticationViews.authenticationDeleteUser,
        name="delete",
    ),
]
