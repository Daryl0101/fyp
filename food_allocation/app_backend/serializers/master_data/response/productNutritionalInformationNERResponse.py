from rest_framework import serializers


class ProductNutritionalInformationNERResponse(serializers.Serializer):
    serving_size = serializers.FloatField()
    calorie = serializers.FloatField()
    carbohydrate = serializers.FloatField()
    protein = serializers.FloatField()
    fat = serializers.FloatField()
    sugar = serializers.FloatField()
    fiber = serializers.FloatField()
    saturated_fat = serializers.FloatField()
    cholesterol = serializers.FloatField()
    sodium = serializers.FloatField()
