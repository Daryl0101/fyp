from rest_framework import serializers


class AllocationInventoryCreateRequest(serializers.Serializer):
    inventory_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    max_quantity_per_family = serializers.IntegerField()

    def validate(self, data):
        if data["inventory_id"] <= 0:
            raise serializers.ValidationError("Inventory ID must be greater than 0")
        if data["quantity"] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        if data["max_quantity_per_family"] > data["quantity"]:
            raise serializers.ValidationError(
                "Max quantity per family must be less than or equal to quantity"
            )
        return data


class AllocationCreateRequest(serializers.Serializer):
    inventories = serializers.ListField(child=AllocationInventoryCreateRequest())
    family_ids = serializers.ListField(child=serializers.IntegerField())
    # min_product_category = serializers.IntegerField()
    allocation_days = serializers.IntegerField()
    diversification = serializers.IntegerField()

    def validate(self, data):
        if len(data["inventories"]) <= 0:
            raise serializers.ValidationError("At least 1 inventory is required")
        if len(data["inventories"]) != len(
            set(item["inventory_id"] for item in data["inventories"])
        ):
            raise serializers.ValidationError("Inventories must be unique")
        if len(data["family_ids"]) <= 0:
            raise serializers.ValidationError("At least 1 family is required")
        if len(data["family_ids"]) != len(set(data["family_ids"])):
            raise serializers.ValidationError("Family IDs must be unique")
        # if data["min_product_category"] < 1:
        #     raise serializers.ValidationError(
        #         "Min product category must be greater than 0"
        #     )
        if data["allocation_days"] < 1:
            raise serializers.ValidationError("Allocation days must be greater than 0")
        if data["diversification"] < 1 or data["diversification"] > 10:
            raise serializers.ValidationError(
                "Diversification must be between 1 and 10"
            )
        return data
