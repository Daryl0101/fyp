from rest_framework import serializers

from app_backend.models.package.package import Package
from app_backend.models.package.package_history import PackageHistory
from app_backend.models.package.package_item import PackageItem
from app_backend.serializers.inventory_management.response.inventorySearchResponse import (
    InventorySearchItemResponse,
)


class PackageItemResponse(serializers.ModelSerializer):
    inventory = InventorySearchItemResponse()

    class Meta:
        model = PackageItem
        fields = "__all__"


class PackageHistoryResponse(serializers.ModelSerializer):
    created_by = serializers.CharField(read_only=True)
    modified_by = serializers.CharField(read_only=True)

    class Meta:
        model = PackageHistory
        exclude = ("package",)


class PackageDetailResponse(serializers.ModelSerializer):
    package_items = PackageItemResponse(many=True)
    package_histories = PackageHistoryResponse(many=True)
    allocation_no = serializers.CharField(
        source="allocation_family.allocation.allocation_no"
    )
    family_no = serializers.CharField(source="family.family_no")

    class Meta:
        model = Package
        exclude = ("allocation_family", "family", "allocation")
