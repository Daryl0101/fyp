from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Add new modules here
sectionpatterns = [
    path("authentication/", include("app_backend.url_paths.authentication_urls")),
    path("master-data/", include("app_backend.url_paths.master_data_urls")),
    path("system-reference/", include("app_backend.url_paths.system_reference_urls")),
    path(
        "inventory-management/",
        include("app_backend.url_paths.inventory_management_urls"),
    ),
    path("allocation/", include("app_backend.url_paths.allocation_urls")),
    path("package/", include("app_backend.url_paths.package_urls")),
]

urlpatterns = [
    path("v1/", include((sectionpatterns, "v1"))),
    # region Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # endregion
]
