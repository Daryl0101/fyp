from django.urls import path

from app_backend.views import systemReferenceViews


urlpatterns = [
    path(
        "food_category",
        systemReferenceViews.foodCategoriesSearch,
        name="search-food-categories",
    ),
]
