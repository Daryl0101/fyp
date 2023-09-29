from rest_framework import serializers

from app_backend.models.master_data.product import Product


class ProductDetailResponse(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
