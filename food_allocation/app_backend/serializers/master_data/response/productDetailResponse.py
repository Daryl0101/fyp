from rest_framework import serializers

from app_backend.models.master_data.product import Product
from app_backend.models.system_reference.food_category import FoodCategory


class ProductFoodCategoryDetailResponse(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ["id", "name", "description"]


class ProductDetailResponse(serializers.ModelSerializer):
    food_categories = ProductFoodCategoryDetailResponse(many=True)

    class Meta:
        model = Product
        fields = "__all__"
