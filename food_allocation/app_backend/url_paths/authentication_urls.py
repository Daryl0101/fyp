from django.urls import path
from app_backend.views import authentication_views

urlpatterns = [
    path("register", authentication_views.authenticationRegister, name="register"),
    path("login", authentication_views.authenticationLogin, name="login"),
    path("logout", authentication_views.authenticationLogout, name="logout"),
    path("profile", authentication_views.authenticationDisplayProfile, name="profile"),
    path("search", authentication_views.authenticationSearchUser, name="search"),
    path(
        "details/<uuid:user_id>",
        authentication_views.authenticationUserDetails,
        name="details",
    ),
    path(
        "update/<uuid:user_id>",
        authentication_views.authenticationUpdateUser,
        name="update",
    ),
    path(
        "delete/<uuid:user_id>",
        authentication_views.authenticationDeleteUser,
        name="delete",
    ),
]
