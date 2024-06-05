from rest_framework import serializers

from app_backend.models.master_data.nutritional_label import NutritionalLabel


class ProductNutritionalInformationNERRequest(serializers.ModelSerializer):
    # image = serializers.ImageField()
    class Meta:
        model = NutritionalLabel
        fields = "__all__"
