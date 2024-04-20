from django.urls import include, path

from app_backend.views import package_views

urlpatterns = [
    path(
        "search",
        package_views.packageSearch,
        name="search-packages",
    ),
    path(
        "<int:package_id>",
        package_views.packageDetails,
        name="view-package",
    ),
    path(
        "<int:package_id>/pack",
        package_views.packagePack,
        name="pack-package",
    ),
    path(
        "<int:package_id>/deliver",
        package_views.packageDeliver,
        name="deliver-package",
    ),
    path(
        "<int:package_id>/cancel",
        package_views.packageCancel,
        name="cancel-package",
    ),
    path(
        "delivered-count/dashboard",
        package_views.packageDeliveredCountDashboard,
        name="packages-delivered-count-dashboard",
    ),
]
