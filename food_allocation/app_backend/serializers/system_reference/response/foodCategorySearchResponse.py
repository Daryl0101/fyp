from rest_framework import serializers
from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.serializers.base.response.paginationResponse import PaginationResponse


class FoodCategorySearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ["id", "name", "description"]


class FoodCategorySearchResponse(PaginationResponse, serializers.Serializer):
    food_categories = FoodCategorySearchItemResponse(many=True)
