# @transaction.atomic
from datetime import date
from channels.consumer import get_channel_layer
from channels.generic.websocket import async_to_sync
from django.db import transaction
from rest_framework import serializers

from app_backend.enums import (
    ActionType,
    AllocationFamilyStatus,
    AllocationStatus,
    ItemNoPrefix,
)
from app_backend.models.allocation.allocation import Allocation
from app_backend.models.allocation.allocation_family import AllocationFamily
from app_backend.models.allocation.allocation_family_inventory import (
    AllocationFamilyInventory,
)
from app_backend.models.allocation.allocation_inventory import AllocationInventory
from app_backend.serializers.allocation.request.allocationCreateRequest import (
    AllocationCreateRequest,
)
from app_backend.services.inventory_management_services import retrieveInventoriesByIds
from app_backend.services.master_data_services import retrieveFamiliesByIds
from app_backend.services.package_services import createPackageByAllocationFamily
from app_backend.tasks.allocation_tasks import taskProcessStartAllocation
from app_backend.utils import generateItemNoFromId, setCreateUpdateProperty


def processCreateAllocation(request):
    result = False
    request_parsed = AllocationCreateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # confirm all allocations in the db has been either accepted or rejected or failed
    existing_allocations = Allocation.objects.filter(
        status__in=[
            AllocationStatus.CREATED,
            AllocationStatus.ONGOING,
            AllocationStatus.SUCCESS,
        ]
    )
    if existing_allocations.count() > 0:
        raise serializers.ValidationError(
            "There are existing allocations that are not completed"
        )

    # retrieve inventories with validation
    inventories = retrieveInventoriesByIds(
        inventory_ids=[
            item["inventory_id"]
            for item in request_parsed.validated_data["inventories"]
        ],
        is_validation_required=True,
    )

    # retrieve families with validation
    families = retrieveFamiliesByIds(
        family_ids=request_parsed.validated_data["family_ids"],
        is_validation_required=True,
    )

    with transaction.atomic():
        # create allocation, set status as STATUS.CREATED, save
        allocation = Allocation(
            status=AllocationStatus.CREATED,
            # min_product_category=request_parsed.validated_data["min_product_category"],
            allocation_days=request_parsed.validated_data["allocation_days"],
            diversification=request_parsed.validated_data["diversification"],
        )
        setCreateUpdateProperty(
            model=allocation, userObject=request.user, actionType=ActionType.CREATE
        )
        allocation.save()
        allocation.allocation_no = generateItemNoFromId(
            prefix=ItemNoPrefix.ALLOCATION, id=allocation.id
        )
        allocation.save()

        # create allocation family, save
        allocation_families = []
        for f in families:
            allocation_family = AllocationFamily(
                allocation=allocation,
                family=f,
            )
            setCreateUpdateProperty(
                model=allocation_family,
                userObject=request.user,
                actionType=ActionType.CREATE,
            )
            allocation_family.save()
            allocation_families.append(allocation_family)

        # dealing with inventories
        allocation_inventories = []
        for i in inventories:
            i_req = next(
                (
                    item
                    for item in request_parsed.validated_data["inventories"]
                    if item["inventory_id"] == i.id
                ),
                None,
            )
            if i_req is None:
                raise serializers.ValidationError("Invalid Inventory")
            # validate quantity for each inventory
            if i.available_qty <= 0 or i.available_qty < i_req["quantity"]:
                raise serializers.ValidationError(
                    "Inventory does not have enough quantity"
                )
            # validate inventories are not expired
            if i.expiration_date <= date.today():
                raise serializers.ValidationError("Inventory is expired")
            # create allocation inventory, save
            allocation_inventory = AllocationInventory(
                allocation=allocation,
                inventory=i,
                quantity=i_req["quantity"],
                max_quantity_per_family=i_req["max_quantity_per_family"],
            )
            setCreateUpdateProperty(
                model=allocation_inventory,
                userObject=request.user,
                actionType=ActionType.CREATE,
            )
            allocation_inventory.save()
            allocation_inventories.append(allocation_inventory)

    # start allocation
    taskProcessStartAllocation.delay(allocation_id=allocation.id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "allocation",
        {
            "type": "allocation_process",
            "message": "New Allocation has been created",
        },
    )
    result = True
    return result


@transaction.atomic
def processAcceptAllocationFamily(request, allocation_family_id):
    result = False
    # validate allocation_family_id
    if allocation_family_id <= 0:
        raise serializers.ValidationError("Allocation Family ID must be greater than 0")
    # retrieve allocation_family
    allocation_family = AllocationFamily.objects.filter(id=allocation_family_id).first()
    # validate allocation_family
    if allocation_family is None:
        raise serializers.ValidationError("Invalid Allocation Family")
    if allocation_family.allocation.status != AllocationStatus.SUCCESS:
        raise serializers.ValidationError("Invalid Allocation Status")
    if allocation_family.family.is_active is False:
        raise serializers.ValidationError("Invalid Family")
    # validate allocation_family status is STATUS.SUCCESS
    if allocation_family.status != AllocationFamilyStatus.SERVED:
        raise serializers.ValidationError("Invalid Allocation Family Status")
    # allocation_family_inventories = allocation_family.allocation_family_inventories.all()
    allocation_family_inventories = AllocationFamilyInventory.objects.filter(
        allocation_family=allocation_family
    )
    for afi in allocation_family_inventories:
        if afi.inventory.expiration_date <= date.today():
            raise serializers.ValidationError("Inventory is expired")
        if afi.inventory.available_qty < afi.quantity:
            raise serializers.ValidationError(
                "Inventory has not enough Available Quantity"
            )
    # create packing job / outbound request
    createPackageByAllocationFamily(
        allocation_family=allocation_family, user=request.user
    )
    # update allocation_family status to STATUS.ACCEPTED, save
    allocation_family.status = AllocationFamilyStatus.ACCEPTED
    allocation_family.save()
    # update allocation status to AllocationStatus.COMPLETED if allocation_family is the last accepted family, save
    if (
        AllocationFamily.objects.filter(
            allocation=allocation_family.allocation,
            status__in=[
                AllocationFamilyStatus.ACCEPTED,
                AllocationFamilyStatus.REJECTED,
                AllocationFamilyStatus.NOT_SERVED,
            ],
        ).count()
        == allocation_family.allocation.allocation_families.count()
    ):
        allocation_family.allocation.status = AllocationStatus.COMPLETED
        allocation_family.allocation.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "allocation",
        {
            "type": "accept_reject_allocation_family",
            "message": None,
        },
    )
    result = True
    return result
