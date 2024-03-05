from datetime import date
from rest_framework import serializers


class InventoryInboundRequest(serializers.Serializer):
    product_id = serializers.IntegerField()
    storage_id = serializers.IntegerField()
    expiration_date = serializers.DateField()
    received_date = serializers.DateField()
    total_qty = serializers.IntegerField()
    num_of_serving = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        if data["expiration_date"] <= date.today():
            raise serializers.ValidationError("Expiration date must be in the future")
        if data["received_date"] > date.today():
            raise serializers.ValidationError("Received date cannot be in the future")
        if data["received_date"] >= data["expiration_date"]:
            raise serializers.ValidationError(
                "Received date cannot be later than or equal to expiration date"
            )
        if data["total_qty"] <= 0:
            raise serializers.ValidationError("Total quantity must be greater than 0")
        if data["num_of_serving"] <= 0:
            raise serializers.ValidationError(
                "Number of serving must be greater than 0"
            )
        return data
