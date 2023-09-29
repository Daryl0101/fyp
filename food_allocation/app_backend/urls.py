from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

sectionpatterns = [
    path("authentication/", include("app_backend.url_paths.authenticationUrls")),
    path("master-data/", include("app_backend.url_paths.masterDataUrls")),
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
