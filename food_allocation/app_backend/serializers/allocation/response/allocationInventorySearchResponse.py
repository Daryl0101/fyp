from rest_framework import serializers

from app_backend.models.allocation.allocation_inventory import AllocationInventory
from app_backend.serializers.base.response.paginationResponse import PaginationResponse
from app_backend.serializers.inventory_management.response.inventoryShortSearchResponse import (
    InventoryShortSearchItemResponse,
)


class AllocationInventorySearchItemResponse(serializers.ModelSerializer):
    inventory = InventoryShortSearchItemResponse()
    created_by = serializers.CharField(read_only=True)
    modified_by = serializers.CharField(read_only=True)

    class Meta:
        model = AllocationInventory
        exclude = ["allocation"]
        # fields = ["id", "inventory", "quantity", "max_quantity_per_family"]


class AllocationInventorySearchResponse(PaginationResponse, serializers.Serializer):
    items = AllocationInventorySearchItemResponse(many=True)
