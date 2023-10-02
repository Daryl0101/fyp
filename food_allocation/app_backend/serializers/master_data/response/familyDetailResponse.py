from rest_framework import serializers

from app_backend.models.master_data.family import Family
from app_backend.models.master_data.person import Person
from app_backend.models.system_reference.food_category import FoodCategory


class FoodRestrictionResponse(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ["id", "name", "description"]


class PersonDetailResponse(serializers.ModelSerializer):
    food_restrictions = FoodRestrictionResponse(many=True)

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
            "food_restrictions",
        ]


class FamilyDetailResponse(serializers.ModelSerializer):
    members = PersonDetailResponse(many=True)

    class Meta:
        model = Family
        fields = "__all__"
