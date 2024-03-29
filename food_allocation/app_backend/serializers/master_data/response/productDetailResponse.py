from rest_framework import serializers

from app_backend.models.master_data.product import Product
from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.serializers.system_reference.response.foodCategorySearchResponse import (
    FoodCategorySearchItemResponse,
)


# class ProductFoodCategoryDetailResponse(serializers.ModelSerializer):
#     class Meta:
#         model = FoodCategory
#         fields = ["id", "name", "description"]


class ProductDetailResponse(serializers.ModelSerializer):
    food_categories = FoodCategorySearchItemResponse(many=True)

    class Meta:
        model = Product
        fields = "__all__"
