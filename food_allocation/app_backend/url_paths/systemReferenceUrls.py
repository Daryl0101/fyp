from django.urls import path

from app_backend.views import systemReferenceViews


urlpatterns = [
    path(
        "food-categories/search",
        systemReferenceViews.foodCategoriesSearch,
        name="search-food-categories",
    ),
    path(
        "storages/search",
        systemReferenceViews.storagesSearch,
        name="search-storages",
    ),
]
