from rest_framework import serializers
from app_backend.models.master_data.product import Product
from app_backend.serializers.base.response.paginationResponse import PaginationResponse


class ProductSearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "product_no", "name", "description", "is_halal"]


class ProductSearchResponse(PaginationResponse, serializers.Serializer):
    items = ProductSearchItemResponse(many=True)
