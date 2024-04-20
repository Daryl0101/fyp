from __future__ import annotations
from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

from app_backend.constants import PERIOD
from app_backend.serializers.base.request.periodIntervalRequest import (
    PeriodIntervalRequest,
)


if TYPE_CHECKING:
    from app_backend.models.master_data.product import Product
    from app_backend.models.system_reference.storage import Storage
    from app_backend.models.authentication.user import User
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import serializers
from app_backend.enums import (
    ActionType,
    HalalStatus,
    InventoryMovement,
    ItemNoPrefix,
    SortOrder,
)
from app_backend.models.inventory_management.inventory import Inventory
from app_backend.models.inventory_management.inventory_history import InventoryHistory
from app_backend.serializers.inventory_management.request.inventoryAdjustRequest import (
    InventoryAdjustRequest,
)
from app_backend.serializers.inventory_management.request.inventoryInboundRequest import (
    InventoryInboundRequest,
)
from app_backend.serializers.inventory_management.request.inventorySearchRequest import (
    InventorySearchRequest,
)
from app_backend.serializers.inventory_management.response.inventoryDetailResponse import (
    InventoryDetailResponse,
)
from app_backend.serializers.inventory_management.response.inventorySearchResponse import (
    InventorySearchItemResponse,
    InventorySearchResponse,
)
from app_backend.utils import generateItemNoFromId, isBlank, setCreateUpdateProperty


# region Public Methods
# Search Live Inventory
def processSearchInventories(request):
    # region Parse request
    request_parsed = InventorySearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    inventories = Inventory.objects.filter(is_active=True)

    if not isBlank(request_parsed.validated_data["inventory_no"]):
        inventories = inventories.filter(
            inventory_no__icontains=request_parsed.validated_data["inventory_no"]
        )

    if not isBlank(request_parsed.validated_data["product_no"]):
        inventories = inventories.filter(
            product__product_no__icontains=request_parsed.validated_data["product_no"]
        )

    if not isBlank(request_parsed.validated_data["product_name"]):
        inventories = inventories.filter(
            product__name__icontains=request_parsed.validated_data["product_name"]
        )

    if not isBlank(request_parsed.validated_data["storage_no"]):
        inventories = inventories.filter(
            storage__storage_no__icontains=request_parsed.validated_data["storage_no"]
        )

    if not isBlank(request_parsed.validated_data["storage_description"]):
        inventories = inventories.filter(
            storage__description__icontains=request_parsed.validated_data[
                "storage_description"
            ]
        )

    if (
        request_parsed.validated_data["expiration_date_start"] is not None
        and request_parsed.validated_data["expiration_date_end"] is not None
    ):
        inventories = inventories.filter(
            expiration_date__range=(
                request_parsed.validated_data["expiration_date_start"],
                request_parsed.validated_data["expiration_date_end"],
            )
        )

    if (
        request_parsed.validated_data["received_date_start"] is not None
        and request_parsed.validated_data["received_date_end"] is not None
    ):
        inventories = inventories.filter(
            received_date__range=(
                request_parsed.validated_data["received_date_start"],
                request_parsed.validated_data["received_date_end"],
            )
        )

    if request_parsed.validated_data["halal_status"] == HalalStatus.HALAL:
        inventories = inventories.filter(product__is_halal=True)
    elif request_parsed.validated_data["halal_status"] == HalalStatus.NON_HALAL:
        inventories = inventories.filter(product__is_halal=False)

    if request_parsed.validated_data["allowed_for_allocation_only"]:
        inventories = inventories.filter(
            available_qty__gt=0, expiration_date__gt=date.today()
        )
    # endregion

    # region Sort
    fields = InventorySearchItemResponse().fields
    scso = "expiration_date"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    inventories = inventories.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=inventories, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = InventorySearchResponse(
        data={
            "items": InventorySearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": (
                page.previous_page_number() if page.has_previous() else None
            ),
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data


# View Live Inventory
def processViewInventory(request, inventory_id: int):
    if inventory_id <= 0:
        raise serializers.ValidationError("Invalid Inventory id")
    inventory = Inventory.objects.filter(is_active=True, id=inventory_id).first()
    if inventory is None:
        raise serializers.ValidationError("Invalid Inventory")
    response_serializer = InventoryDetailResponse(data=inventory)
    return response_serializer.initial_data


# Adjustment
@transaction.atomic
def processAdjustInventory(request, inventory_id: int):
    result = False

    request_parsed = InventoryAdjustRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    if inventory_id <= 0:
        raise serializers.ValidationError("Invalid Inventory ID")
    inventory = (
        Inventory.objects.filter(is_active=True, id=inventory_id)
        .select_for_update()
        .first()
    )
    if inventory is None:
        raise serializers.ValidationError("Invalid Inventory")
    # if inventory.available_qty == 0:
    #     raise serializers.ValidationError("Inventory has no available quantity")

    if request_parsed.validated_data[
        "qty"
    ] == inventory.total_qty or request_parsed.validated_data["qty"] < (
        inventory.total_qty - inventory.available_qty
    ):
        raise serializers.ValidationError("Invalid Quantity")

    before = inventory.total_qty
    inventory.total_qty = request_parsed.validated_data["qty"]
    inventory.available_qty = inventory.available_qty - (before - inventory.total_qty)

    if inventory.total_qty == 0:
        inventory.is_active = False

    setCreateUpdateProperty(inventory, request.user, ActionType.UPDATE)
    inventory.save()

    createInventoryHistory(
        inventory,
        request.user,
        before,
        inventory.total_qty,
        InventoryMovement.ADJUSTMENT,
        request_parsed.validated_data["reason"],
    )

    result = True
    return result


@transaction.atomic
def processDeleteInventory(request, inventory_id: int):
    result = False

    request_parsed = InventoryAdjustRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)

    if inventory_id <= 0:
        raise serializers.ValidationError("Invalid Inventory ID")
    inventory = (
        Inventory.objects.filter(is_active=True, id=inventory_id)
        .select_for_update()
        .first()
    )
    if inventory is None:
        raise serializers.ValidationError("Invalid Inventory")

    if inventory.total_qty > 0 and inventory.total_qty != inventory.available_qty:
        raise serializers.ValidationError(
            "Inventory cannot be deleted because it has packing task(s) associated with it."
        )

    before = inventory.total_qty
    inventory.total_qty = inventory.available_qty = 0
    inventory.is_active = False
    setCreateUpdateProperty(inventory, request.user, ActionType.UPDATE)
    inventory.save()

    createInventoryHistory(
        inventory,
        request.user,
        before,
        0,
        InventoryMovement.ADJUSTMENT,
        request_parsed.validated_data["reason"],
    )

    result = True
    return result


def processViewInboundJobsCountDashboard(request):
    # region Parse request
    request_parsed = PeriodIntervalRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    inventories_count = InventoryHistory.objects.filter(
        movement=InventoryMovement.INBOUND,
        created_at__range=(
            datetime.combine(
                date.today()
                - timedelta(days=PERIOD[request_parsed.validated_data["period"]]),
                time.min,
            ).astimezone(),
            datetime.combine(date.today(), time.max).astimezone(),
        ),
    ).count()

    return inventories_count


# endregion


# region Private Methods

# endregion


def inboundInventoryFromProductStorageAndInventoryInboundRequest(
    product: Product,
    storage: Storage,
    request_parsed: InventoryInboundRequest,
    user: User,
) -> Inventory:
    inventory = Inventory(
        product=product,
        storage=storage,
        expiration_date=request_parsed.validated_data["expiration_date"],
        received_date=request_parsed.validated_data["received_date"],
        total_qty=request_parsed.validated_data["total_qty"],
        available_qty=request_parsed.validated_data["total_qty"],
        num_of_serving=request_parsed.validated_data["num_of_serving"],
    )
    setCreateUpdateProperty(inventory, user, ActionType.CREATE)
    inventory.save()

    inventory.inventory_no = generateItemNoFromId(ItemNoPrefix.INVENTORY, inventory.id)
    inventory.save()

    createInventoryHistory(
        inventory, user, 0, inventory.total_qty, InventoryMovement.INBOUND, ""
    )

    return inventory


# parent function calling this must have @transaction.atomic
def createInventoryHistory(
    inventory: Inventory,
    user: User,
    before: int,
    after: int,
    movement: InventoryMovement,
    reason: str,
):
    inventory_history = InventoryHistory(
        inventory=inventory,
        before=before,
        after=after,
        difference=after - before,
        movement=movement,
        reason=reason,
    )
    setCreateUpdateProperty(inventory_history, user, ActionType.CREATE)
    inventory_history.save()


def retrieveInventoriesByProduct(
    product: Product, is_validation_required: bool
) -> list[Inventory]:
    if product is None:
        raise serializers.ValidationError("Invalid Product")
    inventories = Inventory.objects.filter(is_active=True, product=product)
    if is_validation_required and (inventories is None or len(inventories) <= 0):
        raise serializers.ValidationError("Invalid Inventories")
    return inventories


def retrieveInventoriesByProductAndStorage(
    product: Product, storage: Storage, is_validation_required: bool
) -> list[Inventory]:
    if product is None:
        raise serializers.ValidationError("Invalid Product")
    if storage is None:
        raise serializers.ValidationError("Invalid Storage")
    inventories = Inventory.objects.filter(
        is_active=True, product=product, storage=storage
    )
    if is_validation_required and (inventories is None or len(inventories) <= 0):
        raise serializers.ValidationError("Invalid Inventories")
    return inventories


def retrieveInventoriesByIds(
    inventory_ids: list[int], is_validation_required: bool
) -> list[Inventory]:
    if (
        len(inventory_ids) <= 0
        or len(set(inventory_ids)) != len(inventory_ids)
        or any(id <= 0 for id in inventory_ids)
    ):
        raise serializers.ValidationError("Invalid Inventory IDs")
    inventories = Inventory.objects.filter(is_active=True, id__in=set(inventory_ids))
    if is_validation_required and (
        inventories is None
        or len(inventories) <= 0
        or len(inventories) != len(set(inventory_ids))
    ):
        raise serializers.ValidationError("Invalid Inventories")
    return inventories
