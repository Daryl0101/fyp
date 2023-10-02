from rest_framework import serializers


class ProductCreateUpdateRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    serving_size = serializers.DecimalField(max_digits=10, decimal_places=2)
    carbs_calorie = serializers.DecimalField(max_digits=10, decimal_places=2)
    protein_calorie = serializers.DecimalField(max_digits=10, decimal_places=2)
    fat_calorie = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_halal = serializers.BooleanField()
    food_categories = serializers.ListField(child=serializers.IntegerField())

    def validate(self, data):
        if data["serving_size"] <= 0:
            raise serializers.ValidationError("Serving size must be greater than 0")
        if data["carbs_calorie"] < 0:
            raise serializers.ValidationError("Invalid Carbohydrate calorie")
        if data["protein_calorie"] < 0:
            raise serializers.ValidationError("Invalid Protein calorie")
        if data["fat_calorie"] < 0:
            raise serializers.ValidationError("Invalid Fat calorie")
        if data["carbs_calorie"] + data["protein_calorie"] + data["fat_calorie"] <= 0:
            raise serializers.ValidationError(
                "Food has no calories. Please check your input."
            )
        if len(data["food_categories"]) <= 0:
            raise serializers.ValidationError("At least 1 food category is required")
        if list(filter(lambda x: x <= 0, data["food_categories"])):
            raise serializers.ValidationError("Invalid food category id(s)")
        if len(set(data["food_categories"])) != len(data["food_categories"]):
            raise serializers.ValidationError("Duplicate food category ids detected")
        return data
