from app_backend.models.inventory_management.inventory import Inventory
from rest_framework import serializers


class InventoryShortSearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            "id",
            "inventory_no",
            "total_qty",
            "available_qty",
            "expiration_date",
            "received_date",
            "is_active",
        ]
