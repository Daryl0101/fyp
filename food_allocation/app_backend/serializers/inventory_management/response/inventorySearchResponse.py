from rest_framework import serializers
from app_backend.models.inventory_management.inventory import Inventory

from app_backend.serializers.base.response.paginationResponse import PaginationResponse
from app_backend.serializers.master_data.response.productSearchResponse import (
    ProductSearchItemResponse,
)
from app_backend.serializers.system_reference.response.storageSearchResponse import (
    StorageSearchItemResponse,
)


class InventorySearchItemResponse(serializers.ModelSerializer):
    product = ProductSearchItemResponse()
    storage = StorageSearchItemResponse()

    class Meta:
        model = Inventory
        fields = [
            "id",
            "inventory_no",
            "product",
            "storage",
            "expiration_date",
            "received_date",
            "total_qty",
            "available_qty",
        ]


class InventorySearchResponse(PaginationResponse, serializers.Serializer):
    items = InventorySearchItemResponse(many=True)
