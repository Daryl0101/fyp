from rest_framework import serializers
from app_backend.models.allocation.allocation_family import AllocationFamily
from app_backend.models.allocation.allocation_family_inventory import (
    AllocationFamilyInventory,
)
from app_backend.serializers.base.response.paginationResponse import PaginationResponse
from app_backend.serializers.inventory_management.response.inventoryShortSearchResponse import (
    InventoryShortSearchItemResponse,
)
from app_backend.serializers.master_data.response.familySearchResponse import (
    FamilySearchItemResponse,
)


class AllocationFamilyInventoryItemSearchResponse(serializers.ModelSerializer):
    inventory = InventoryShortSearchItemResponse()

    class Meta:
        model = AllocationFamilyInventory
        fields = ["inventory", "quantity"]


class AllocationFamilyItemSearchResponse(serializers.ModelSerializer):
    family = FamilySearchItemResponse()
    allocation_family_inventories = AllocationFamilyInventoryItemSearchResponse(
        many=True
    )
    created_by = serializers.CharField(read_only=True)
    modified_by = serializers.CharField(read_only=True)

    class Meta:
        model = AllocationFamily
        exclude = ["allocation", "inventories"]
        # fields = ["id", "family", "allocation_family_inventories"]


class AllocationFamilySearchResponse(PaginationResponse, serializers.Serializer):
    items = AllocationFamilyItemSearchResponse(many=True)
