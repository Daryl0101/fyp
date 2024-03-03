from rest_framework import serializers


class ProductCreateUpdateRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(
        max_length=255, allow_blank=True, required=False, default=""
    )
    serving_size = serializers.DecimalField(max_digits=10, decimal_places=2)
    calorie = serializers.DecimalField(max_digits=10, decimal_places=2)  # kcal
    carbohydrate = serializers.DecimalField(max_digits=10, decimal_places=2)  # g
    protein = serializers.DecimalField(max_digits=10, decimal_places=2)  # g
    fat = serializers.DecimalField(max_digits=10, decimal_places=2)  # g
    fiber = serializers.DecimalField(max_digits=10, decimal_places=2)  # g
    sugar = serializers.DecimalField(max_digits=10, decimal_places=2)  # g
    saturated_fat = serializers.DecimalField(max_digits=10, decimal_places=2)  # g
    cholesterol = serializers.DecimalField(max_digits=10, decimal_places=2)  # mg
    sodium = serializers.DecimalField(max_digits=10, decimal_places=2)  # mg
    is_halal = serializers.BooleanField()
    food_categories = serializers.ListField(child=serializers.IntegerField())

    def validate(self, data):
        if data["serving_size"] <= 0:
            raise serializers.ValidationError("Serving size must be greater than 0")
        if data["calorie"] < 0:
            raise serializers.ValidationError("Invalid Calorie amount")
        if data["carbohydrate"] < 0:
            raise serializers.ValidationError("Invalid Carbohydrate amount")
        if data["protein"] < 0:
            raise serializers.ValidationError("Invalid Protein amount")
        if data["fat"] < 0:
            raise serializers.ValidationError("Invalid Fat amount")
        if data["fiber"] < 0:
            raise serializers.ValidationError("Invalid Fiber amount")
        if data["sugar"] < 0:
            raise serializers.ValidationError("Invalid Sugar amount")
        if data["saturated_fat"] < 0:
            raise serializers.ValidationError("Invalid Saturated Fat amount")
        if data["cholesterol"] < 0:
            raise serializers.ValidationError("Invalid Cholesterol amount")
        if data["sodium"] < 0:
            raise serializers.ValidationError("Invalid Sodium amount")
        if data["calorie"] + data["carbohydrate"] + data["protein"] + data["fat"] <= 0:
            raise serializers.ValidationError(
                "Food has no nutritional content. Please check your input."
            )
        if len(data["food_categories"]) <= 0:
            raise serializers.ValidationError("At least 1 food category is required")
        if list(filter(lambda x: x <= 0, data["food_categories"])):
            raise serializers.ValidationError("Invalid food category id(s)")
        if len(set(data["food_categories"])) != len(data["food_categories"]):
            raise serializers.ValidationError("Duplicate food category ids detected")
        return data
