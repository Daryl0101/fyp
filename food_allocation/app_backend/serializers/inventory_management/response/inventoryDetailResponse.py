from rest_framework import serializers
from app_backend.models.inventory_management.inventory import Inventory


class InventoryDetailResponse(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
