from rest_framework import serializers


class InventoryAdjustRequest(serializers.Serializer):
    qty = serializers.IntegerField(default=0)
    reason = serializers.CharField(max_length=200)
