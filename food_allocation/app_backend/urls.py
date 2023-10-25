from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Add new modules here
sectionpatterns = [
    path("authentication/", include("app_backend.url_paths.authenticationUrls")),
    path("master-data/", include("app_backend.url_paths.masterDataUrls")),
    path("system-reference/", include("app_backend.url_paths.systemReferenceUrls")),
    path(
        "inventory-management/",
        include("app_backend.url_paths.inventoryManagementUrls"),
    ),
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
