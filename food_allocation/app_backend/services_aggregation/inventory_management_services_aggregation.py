# Inbound
from django.db import transaction
from rest_framework import serializers
from app_backend.enums import InventoryMovement, ItemNoPrefix

from app_backend.serializers.inventory_management.request.inventoryInboundRequest import (
    InventoryInboundRequest,
)
from app_backend.services.inventory_management_services import (
    inboundInventoryFromProductStorageAndInventoryInboundRequest,
    retrieveInventoriesByProductAndStorage,
)
from app_backend.services.master_data_services import retrieveActiveProductById
from app_backend.services.system_reference_services import retrieveActiveStorageById


@transaction.atomic
def processInboundInventory(request):
    result = False

    request_parsed = InventoryInboundRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    product = retrieveActiveProductById(
        request_parsed.validated_data["product_id"], True
    )
    storage = retrieveActiveStorageById(
        request_parsed.validated_data["storage_id"], True
    )

    if product.is_halal != storage.is_halal:
        raise serializers.ValidationError(
            "The product and storage must have the same halal status."
        )

    inventories = retrieveInventoriesByProductAndStorage(
        product=product, storage=storage, is_validation_required=False
    )
    if inventories is not None and len(inventories) > 0:
        raise serializers.ValidationError(
            "This product already exists in this storage. Choose another storage or product."
        )

    inboundInventoryFromProductStorageAndInventoryInboundRequest(
        product=product,
        storage=storage,
        request_parsed=request_parsed,
        user=request.user,
    )

    result = True
    return result
