from rest_framework import serializers

from app_backend.models.master_data.family import Family
from app_backend.models.master_data.person import Person
from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.serializers.system_reference.response.foodCategorySearchResponse import (
    FoodCategorySearchItemResponse,
)


# class FoodRestrictionResponse(serializers.ModelSerializer):
#     class Meta:
#         model = FoodCategory
#         fields = ["id", "name", "description"]


class PersonDetailResponse(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "birthdate",
            "height",
            "weight",
            "activity_level",
        ]


class FamilyDetailResponse(serializers.ModelSerializer):
    food_restrictions = FoodCategorySearchItemResponse(many=True)
    members = PersonDetailResponse(many=True)

    class Meta:
        model = Family
        fields = "__all__"
