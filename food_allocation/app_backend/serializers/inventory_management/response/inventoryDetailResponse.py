from rest_framework import serializers
from app_backend.models.inventory_management.inventory import Inventory
from app_backend.serializers.master_data.response.productDetailResponse import (
    ProductDetailResponse,
)
from app_backend.serializers.system_reference.response.storageDetailResponse import (
    StorageDetailResponse,
)


class InventoryDetailResponse(serializers.ModelSerializer):
    product = ProductDetailResponse()
    storage = StorageDetailResponse()

    class Meta:
        model = Inventory
        fields = "__all__"
