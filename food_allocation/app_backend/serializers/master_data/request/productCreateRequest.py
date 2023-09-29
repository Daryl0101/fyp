from rest_framework import serializers


class ProductCreateUpdateRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    serving_size = serializers.DecimalField(max_digits=10, decimal_places=2)
    carbs_calorie = serializers.DecimalField(max_digits=10, decimal_places=2)
    protein_calorie = serializers.DecimalField(max_digits=10, decimal_places=2)
    fat_calorie = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_halal = serializers.BooleanField()

    def validate(self, data):
        if data["serving_size"] <= 0:
            raise serializers.ValidationError("Serving size must be greater than 0")
        if data["carbs_calorie"] + data["protein_calorie"] + data["fat_calorie"] <= 0:
            raise serializers.ValidationError(
                "Food has no calories. Please check your input."
            )
        return data
