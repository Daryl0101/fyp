from rest_framework import serializers

from app_backend.models.allocation.allocation import Allocation
from app_backend.models.allocation.allocation_inventory import AllocationInventory
from app_backend.models.inventory_management.inventory import Inventory


# class AllocationInventoryQuantityResponse(serializers.ModelSerializer):
#     class Meta:
#         model = AllocationInventory
#         fields = ["quantity"]


# class InventoryWithAllocationQuantityResponse(serializers.ModelSerializer):
#     allocation_inventory = AllocationInventoryQuantityResponse()

#     class Meta:
#         model = Inventory
#         fields = ["inventory_no", "allocation_inventory"]


class AllocationDetailResponse(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        exclude = ["inventories", "families"]
