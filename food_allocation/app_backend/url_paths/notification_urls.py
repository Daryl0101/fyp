from django.urls import include, path

from app_backend.views import notification_views

urlpatterns = [
    path(
        "mark-as-read",
        notification_views.notificationMarkAsRead,
        name="read-notification",
    ),
    path(
        "<str:notification_id>/delete",
        notification_views.notificationDelete,
        name="delete-notification",
    ),
    path(
        "fcm/register",
        notification_views.registerUserFCMToken,
        name="register-fcm-token",
    ),
    path(
        "fcm/unregister",
        notification_views.unregisterUserFCMToken,
        name="unregister-fcm-token",
    ),
]
