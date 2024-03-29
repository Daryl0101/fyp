from django.urls import path

from app_backend.views import system_reference_views


urlpatterns = [
    path(
        "food-categories/search",
        system_reference_views.foodCategoriesSearch,
        name="search-food-categories",
    ),
    path(
        "storages/search",
        system_reference_views.storagesSearch,
        name="search-storages",
    ),
    path(
        "storages/<int:storage_id>",
        system_reference_views.storageDetails,
        name="search-storages",
    ),
]
