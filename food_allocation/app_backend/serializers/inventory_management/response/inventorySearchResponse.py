from rest_framework import serializers
from app_backend.models.inventory_management.inventory import Inventory

from app_backend.serializers.base.response.paginationResponse import PaginationResponse


class InventorySearchItemResponse(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")
    storage_name = serializers.CharField(source="storage.name")
    # received_date = serializers.DateTimeField(source="received_date")

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product_name",
            "storage_name",
            "expiration_date",
            "received_date",
            "total_qty",
            "available_qty",
        ]


class InventorySearchResponse(PaginationResponse, serializers.Serializer):
    items = InventorySearchItemResponse(many=True)
