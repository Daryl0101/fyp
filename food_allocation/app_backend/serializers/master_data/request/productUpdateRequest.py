from rest_framework import serializers


class ProductUpdateRequest(serializers.Serializer):
    serving_size = serializers.DecimalField(max_digits=10, decimal_places=2, default=1)
    calorie = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # kcal
    carbohydrate = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # g
    protein = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)  # g
    fat = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)  # g
    fiber = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)  # g
    sugar = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)  # g
    saturated_fat = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # g
    cholesterol = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # mg
    sodium = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)  # mg

    def validate(self, data):
        if data["serving_size"] <= 0:
            raise serializers.ValidationError("Serving size must be greater than 0")
        if data["calorie"] <= 0:
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
        if data["carbohydrate"] + data["protein"] + data["fat"] <= 0:
            raise serializers.ValidationError(
                "Food has no nutritional content. Please check your input."
            )
        return data
