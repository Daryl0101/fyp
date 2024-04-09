from __future__ import annotations
import collections
import decimal
import functools
import operator
from typing import TYPE_CHECKING, TypedDict

from channels.consumer import get_channel_layer
from channels.generic.websocket import async_to_sync
from django.db.models import QuerySet

from app_backend.models.allocation.allocation_family_inventory import (
    AllocationFamilyInventory,
)
from app_backend.serializers.allocation.response.allocationIsAllowedValidationResponse import (
    AllocationIsAllowedValidationResponse,
)
from app_backend.services.allocation_processes import (
    AllocationProcessResult,
    allocationProcess,
)


if TYPE_CHECKING:
    from app_backend.models.master_data.family import Family
from datetime import date
from datetime import datetime
from django.core.paginator import Paginator
from rest_framework import serializers
from django.db import transaction
from app_backend.enums import (
    ActionType,
    AllocationFamilyStatus,
    AllocationStatus,
    Gender,
    SortOrder,
)
from app_backend.models.allocation.allocation import Allocation
from app_backend.models.allocation.allocation_family import AllocationFamily
from app_backend.models.allocation.allocation_inventory import AllocationInventory
from app_backend.serializers.allocation.request.allocationFamilySearchRequest import (
    AllocationFamilySearchRequest,
)
from app_backend.serializers.allocation.request.allocationInventorySearchRequest import (
    AllocationInventorySearchRequest,
)
from app_backend.serializers.allocation.request.allocationSearchRequest import (
    AllocationSearchRequest,
)
from app_backend.serializers.allocation.response.allocationDetailResponse import (
    AllocationDetailResponse,
)
from app_backend.serializers.allocation.response.allocationFamilySearchResponse import (
    AllocationFamilyItemSearchResponse,
    AllocationFamilySearchResponse,
)
from app_backend.serializers.allocation.response.allocationInventorySearchResponse import (
    AllocationInventorySearchItemResponse,
    AllocationInventorySearchResponse,
)
from app_backend.serializers.allocation.response.allocationSearchResponse import (
    AllocationSearchItemResponse,
    AllocationSearchResponse,
)
from app_backend.utils import isBlank, setCreateUpdateProperty


# region data structure passed to allocation algorithm
class DataDictNutrients(TypedDict):
    calorie: int
    carbohydrate: int
    protein: int
    fat: int
    fiber: int
    sugar: int
    saturated_fat: int
    cholesterol: int
    sodium: int


class DataDictFamilies(TypedDict):
    id: int
    is_halal: bool
    food_restriction_ids: list[int]
    priority: float
    nutrients: DataDictNutrients


class DataDictInventories(TypedDict):
    id: int
    qty: int
    is_halal: bool
    food_category_ids: list[int]
    max_qty_per_family: int
    nutrients: DataDictNutrients


class DataDict(TypedDict):
    families: list[DataDictFamilies]
    inventories: list[DataDictInventories]


# endregion


def processSearchAllocations(request):
    # region Parse request
    request_parsed = AllocationSearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter allocations
    allocations = Allocation.objects.all()

    if not isBlank(request_parsed.validated_data["allocation_no"]):
        allocations = allocations.filter(
            allocation_no__icontains=request_parsed.validated_data["allocation_no"]
        )

    if not isBlank(request_parsed.validated_data["inventory_no"]):
        allocations = allocations.filter(
            inventories__inventory_no__icontains=request_parsed.validated_data[
                "inventory_no"
            ]
        )

    if not isBlank(request_parsed.validated_data["family_no"]):
        allocations = allocations.filter(
            families__family_no__icontains=request_parsed.validated_data["family_no"]
        )

    if not isBlank(request_parsed.validated_data["status"]):
        allocations = allocations.filter(status=request_parsed.validated_data["status"])
    # endregion

    # region Sort
    fields = AllocationSearchItemResponse().fields
    scso = "id"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    allocations = allocations.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=allocations, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = AllocationSearchResponse(
        data={
            "items": AllocationSearchItemResponse(
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


def processSearchAllocationInventories(request):
    request_parsed = AllocationInventorySearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)

    allocation_id = request_parsed.validated_data["allocation_id"]
    if int(allocation_id) < 0:
        raise serializers.ValidationError("Allocation ID must be greater than 0")

    allocation = Allocation.objects.filter(id=allocation_id).first()
    if allocation is None:
        raise serializers.ValidationError("Invalid Allocation")

    allocation_inventories = AllocationInventory.objects.filter(allocation=allocation)

    # region Sort
    fields = AllocationInventorySearchItemResponse().fields
    scso = "id"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    allocation_inventories = allocation_inventories.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=allocation_inventories,
        per_page=request_parsed.validated_data["page_size"],
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = AllocationInventorySearchResponse(
        data={
            "items": AllocationInventorySearchItemResponse(
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


def processSearchAllocationFamilies(request):
    request_parsed = AllocationFamilySearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)

    allocation_id = request_parsed.validated_data["allocation_id"]
    if int(allocation_id) < 0:
        raise serializers.ValidationError("Allocation ID must be greater than 0")

    allocation = Allocation.objects.filter(id=allocation_id).first()
    if allocation is None:
        raise serializers.ValidationError("Invalid Allocation")

    allocation_families = AllocationFamily.objects.filter(allocation=allocation)

    # region Sort
    fields = AllocationFamilyItemSearchResponse().fields
    scso = "id"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    allocation_families = allocation_families.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=allocation_families,
        per_page=request_parsed.validated_data["page_size"],
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = AllocationFamilySearchResponse(
        data={
            "items": AllocationFamilyItemSearchResponse(
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


def processViewAllocation(request, allocation_id):
    if int(allocation_id) <= 0:
        raise serializers.ValidationError("Allocation ID must be greater than 0")
    allocation = Allocation.objects.filter(id=allocation_id).first()
    if allocation is None:
        raise serializers.ValidationError("Invalid Allocation")
    response_serializer = AllocationDetailResponse(data=allocation)
    return response_serializer.initial_data


def processValidateNewAllocationIsAllowed(request):
    result = {"is_allowed": True, "current_allocation": None}
    # retrieve all allocations with status in [STATUS.CREATED, STATUS.ONGOING, STATUS.SUCCESS]
    allocations = Allocation.objects.filter(
        status__in=[
            AllocationStatus.CREATED,
            AllocationStatus.ONGOING,
            AllocationStatus.SUCCESS,
        ]
    )
    if allocations.first() is not None:
        result = {"is_allowed": False, "current_allocation": allocations.first()}
    return AllocationIsAllowedValidationResponse(data=result).initial_data


# This is used in consumer
def processStartAllocation(allocation_id: int):
    result = False

    if allocation_id <= 0:
        raise serializers.ValidationError("Allocation ID must be greater than 0")
    # retrieve allocation
    allocation = Allocation.objects.filter(id=allocation_id).first()
    if allocation is None:
        raise serializers.ValidationError("Invalid Allocation")
    if (
        allocation.status != AllocationStatus.CREATED
        or allocation.start_time is not None
    ):
        raise serializers.ValidationError("Invalid Allocation Status")

    allocation_inventories = AllocationInventory.objects.filter(allocation=allocation)
    if (allocation_inventories.count()) <= 0:
        raise serializers.ValidationError("Invalid Allocation Inventory")
    allocation_families: QuerySet[AllocationFamily] = (
        allocation.allocation_families.all()
    )

    # extract inventories data
    inventories_data: list[DataDictInventories] = []
    for ai in allocation_inventories:
        inventories_data.append(
            {
                "id": ai.inventory.id,
                "qty": ai.quantity,
                "is_halal": ai.inventory.product.is_halal,
                "food_category_ids": [
                    food_category.id
                    for food_category in ai.inventory.product.food_categories.all()
                ],
                "max_qty_per_family": ai.max_quantity_per_family,
                "nutrients": {
                    "calorie": ai.inventory.product.calorie
                    * ai.inventory.num_of_serving,
                    "carbohydrate": ai.inventory.product.carbohydrate
                    * ai.inventory.num_of_serving,
                    "protein": ai.inventory.product.protein
                    * ai.inventory.num_of_serving,
                    "fat": ai.inventory.product.fat * ai.inventory.num_of_serving,
                    "fiber": ai.inventory.product.fiber * ai.inventory.num_of_serving,
                    "sugar": ai.inventory.product.sugar * ai.inventory.num_of_serving,
                    "saturated_fat": ai.inventory.product.saturated_fat
                    * ai.inventory.num_of_serving,
                    "cholesterol": ai.inventory.product.cholesterol
                    * ai.inventory.num_of_serving,
                    "sodium": ai.inventory.product.sodium * ai.inventory.num_of_serving,
                },
            }
        )

    with transaction.atomic():
        # extract families data
        families_data: list[DataDictFamilies] = []
        for af in allocation_families:
            nutrients = __calculateNutrientsRequired(family=af.family)
            af.calorie_needed = nutrients["calorie"] * allocation.allocation_days
            af.carbohydrate_needed = (
                nutrients["carbohydrate"] * allocation.allocation_days
            )
            af.protein_needed = nutrients["protein"] * allocation.allocation_days
            af.fat_needed = nutrients["fat"] * allocation.allocation_days
            af.fiber_needed = nutrients["fiber"] * allocation.allocation_days
            af.sugar_needed = nutrients["sugar"] * allocation.allocation_days
            af.saturated_fat_needed = (
                nutrients["saturated_fat"] * allocation.allocation_days
            )
            af.cholesterol_needed = (
                nutrients["cholesterol"] * allocation.allocation_days
            )
            af.sodium_needed = nutrients["sodium"] * allocation.allocation_days
            # af.status = AllocationFamilyStatus.SERVED
            af.save()
            families_data.append(
                {
                    "id": af.id,
                    "is_halal": af.family.is_halal,
                    "food_restriction_ids": [
                        food_restriction.id
                        for food_restriction in af.family.food_restrictions.all()
                    ],
                    "priority": (af.family.household_income / af.family.total_member),
                    "nutrients": {
                        k: v * allocation.allocation_days
                        for k, v in nutrients.items()  # multiply daily nutrients requirement by planned days
                    },
                }
            )

        # set allocation start time and update allocation status to STATUS.ONGOING
        allocation.start_time = datetime.now()
        allocation.status = AllocationStatus.ONGOING
        allocation.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "allocation",
        {
            "type": "allocation_process",
            "message": "Allocation has started",
        },
    )

    allocation_result = allocationProcess(
        # min_product_category=allocation.min_product_category,
        inventories=inventories_data,
        families=families_data,
        diversification=allocation.diversification,
    )

    processEndAllocation(
        allocation_id=allocation.id, allocation_result=allocation_result
    )

    result = True
    return result


# @transaction.atomic
def processEndAllocation(
    allocation_id: int, allocation_result: AllocationProcessResult
):
    with transaction.atomic():
        # retrieve allocation, allocation_families, inventories
        allocation = (
            Allocation.objects.filter(id=allocation_id).select_for_update().first()
        )
        if allocation is None:
            raise serializers.ValidationError("Invalid Allocation")
        allocation_families = allocation.allocation_families.all()
        inventories = allocation.inventories.all()

        # based on the allocation results, update allocation status to either STATUS.SUCCESSFUL or STATUS.FAILED, including the log result, save
        if allocation_result["status"] == "SUCCESS":
            allocation.status = AllocationStatus.SUCCESS

            # for each allocation_family in the allocation result
            for ar in allocation_result["data"]:
                allocation_family = allocation_families.filter(id=ar.id).first()
                if allocation_family is None:
                    raise serializers.ValidationError("Invalid Allocation Family")

                # get all inventories for the family in current allocation
                current_family_inventories = [
                    (inventories.filter(id=ai.id).first(), ar.allocated_inventories[ai])
                    for ai in ar.allocated_inventories
                ]  # list[tuple[models.inventory.Inventory, int]]

                # case: allocation result is invalid or not allocatable
                if (
                    len(ar.allocated_inventories)
                    <= 0  # there are no inventories allocated in the result
                    or allocation_family.allocation_family_inventories.count()
                    > 0  # there are existing allocation family inventories
                    or any(
                        not i.is_active
                        or i.available_qty < j
                        or i.expiration_date <= date.today()
                        for i, j in current_family_inventories
                    )  # there are inventories that are not active or not enough quantity or inventory has expired
                    or allocation_family.family.is_active
                    is False  # family is not active
                ):
                    allocation_family.status = AllocationFamilyStatus.NOT_SERVED
                    allocation_family.save()
                    continue

                allocation_family.calorie_allocated = (
                    allocation_family.calorie_needed - ar.nutrients["calorie"]
                )
                allocation_family.carbohydrate_allocated = (
                    allocation_family.carbohydrate_needed - ar.nutrients["carbohydrate"]
                )
                allocation_family.protein_allocated = (
                    allocation_family.protein_needed - ar.nutrients["protein"]
                )
                allocation_family.fat_allocated = (
                    allocation_family.fat_needed - ar.nutrients["fat"]
                )
                allocation_family.fiber_allocated = (
                    allocation_family.fiber_needed - ar.nutrients["fiber"]
                )
                allocation_family.sugar_allocated = (
                    allocation_family.sugar_needed - ar.nutrients["sugar"]
                )
                allocation_family.saturated_fat_allocated = (
                    allocation_family.saturated_fat_needed
                    - ar.nutrients["saturated_fat"]
                )
                allocation_family.cholesterol_allocated = (
                    allocation_family.cholesterol_needed - ar.nutrients["cholesterol"]
                )
                allocation_family.sodium_allocated = (
                    allocation_family.sodium_needed - ar.nutrients["sodium"]
                )
                allocation_family.status = AllocationFamilyStatus.SERVED
                allocation_family.save()

                # create allocation_family_inventories
                for ai in current_family_inventories:
                    allocation_family_inventory = AllocationFamilyInventory(
                        allocation_family=allocation_family,
                        inventory=ai[0],
                        quantity=ai[1],
                    )
                    setCreateUpdateProperty(
                        model=allocation_family_inventory,
                        userObject=allocation.created_by,
                        actionType=ActionType.CREATE,
                    )
                    allocation_family_inventory.save()
                    # [DO NOT SAVE THIS INVENTORY (the line below)]
                    # reduce available quantity of the Inventory by the allocated quantity so that upcoming allocations will not allocate the already allocated inventories
                    ai[0].available_qty -= ai[1]
        else:
            for af in allocation_families:
                af.status = AllocationFamilyStatus.NOT_SERVED
                af.save()
            allocation.status = AllocationStatus.FAILED

        allocation.end_time = datetime.now()
        allocation.log = allocation_result["log"]
        allocation.save()

    if allocation.status == AllocationStatus.SUCCESS:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "allocation",
            {
                "type": "allocation_process",
                "message": "Allocation successful",
            },
        )
    else:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "allocation",
            {
                "type": "allocation_process",
                "message": "Allocation failed",
            },
        )


@transaction.atomic
def processRejectAllocationFamily(request, allocation_family_id):
    result = False
    # validate allocation_family_id
    if allocation_family_id <= 0:
        raise serializers.ValidationError("Allocation Family ID must be greater than 0")
    # retrieve allocation_family
    allocation_family = AllocationFamily.objects.filter(id=allocation_family_id).first()
    # validate allocation_family
    if allocation_family is None:
        raise serializers.ValidationError("Invalid Allocation Family")
    # validate allocation status is STATUS.SUCCESS
    if allocation_family.allocation.status != AllocationStatus.SUCCESS:
        raise serializers.ValidationError("Invalid Allocation Status")
    # validate allocation_family status is STATUS.SERVED
    if allocation_family.status != AllocationFamilyStatus.SERVED:
        raise serializers.ValidationError("Invalid Allocation Family Status")
    # update allocation_family status to STATUS.REJECTED, save
    allocation_family.status = AllocationFamilyStatus.REJECTED
    setCreateUpdateProperty(allocation_family, request.user, ActionType.UPDATE)
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
        setCreateUpdateProperty(
            allocation_family.allocation, request.user, ActionType.UPDATE
        )
        allocation_family.allocation.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "allocation",
            {
                "type": "allocation_process",
                "message": "Allocation completed",
            },
        )
    else:
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


@transaction.atomic
def processRejectExpiredAllocationFamilies():
    # retrieve all allocation families with status SERVED and expired inventories
    allocation_families = AllocationFamily.objects.filter(
        status=AllocationFamilyStatus.SERVED,
        inventories__expiration_date__lte=date.today(),
    )
    if not allocation_families.exists():
        return
    for af in allocation_families:
        # update allocation_family status to STATUS.REJECTED, save
        af.status = AllocationFamilyStatus.REJECTED
        setCreateUpdateProperty(af, af.created_by, ActionType.UPDATE)
        # TODO: create a separate account for the system, to differentiate system actions from user actions
        af.save()
        # update allocation status to AllocationStatus.COMPLETED if allocation_family is the last accepted family, save
    channel_layer = get_channel_layer()
    if (
        allocation_families.filter(
            status__in=[
                AllocationFamilyStatus.ACCEPTED,
                AllocationFamilyStatus.REJECTED,
                AllocationFamilyStatus.NOT_SERVED,
            ]
        ).count()
        == allocation_families.count()
    ):
        af.allocation.status = AllocationStatus.COMPLETED
        setCreateUpdateProperty(
            af.allocation, af.allocation.created_by, ActionType.UPDATE
        )
        af.allocation.save()
        async_to_sync(channel_layer.group_send)(
            "allocation",
            {
                "type": "allocation_process",
                "message": "Expired allocation families have been rejected",
            },
        )
        # print("Expired allocation families have been rejected - Allocation completed")
    else:
        async_to_sync(channel_layer.group_send)(
            "allocation",
            {
                "type": "accept_reject_allocation_family",
                "message": None,
            },
        )
        # print(
        #     "Expired allocation families have been rejected - Allocation not completed"
        # )


# Delayed indefinitely
def processAcceptAllocation(request, allocation_id):
    # validate allocation_id
    if allocation_id <= 0:
        raise serializers.ValidationError("Allocation ID must be greater than 0")
    # retrieve allocation
    allocation = Allocation.objects.filter(id=allocation_id).first()
    # validate allocation
    if allocation is None:
        raise serializers.ValidationError("Invalid Allocation")
    # validate allocation status is STATUS.SUCCESS
    if allocation.status != AllocationStatus.SUCCESS:
        raise serializers.ValidationError("Invalid Allocation Status")
    # validate allocation inventories are all active

    # validate allocation inventories are not expired
    # validate allocation inventories have enough quantity to be allocated
    # validate allocation families are all active

    # update allocation status to STATUS.ACCEPTED, save
    # create packing job / outbound request
    pass


# Delayed indefinitely
def processRejectAllocation(request, allocation_id):
    # validate allocation_id
    # retrieve allocation
    # validate allocation
    # validate allocation status is STATUS.SUCCESS
    # update allocation status to STATUS.REJECTED, save
    pass


# region private methods
def __calculateNutrientsRequired(family: Family) -> DataDictNutrients:
    result = []
    members = family.members.all()
    for member in members:
        # BMR calculation (Miffin-St Jeor Equation)
        age = __calculateAge(member.birthdate)
        bmr = 10 * member.weight + decimal.Decimal(6.25) * member.height - 5 * age
        if member.gender == Gender.MALE:
            bmr += 5
        elif member.gender == Gender.FEMALE:
            bmr -= 161
        # TDEE calculation
        tdee = bmr * (
            decimal.Decimal(1.2) + (member.activity_level - 1) * decimal.Decimal(0.175)
        )
        # Nutrients calculation - Daily Recommended Intake (DRI)
        nutrient = None
        if age <= 3:
            nutrient = {
                "calorie": tdee * (100 - family.calorie_discount) / 100,
                "carbohydrate": tdee
                * decimal.Decimal(0.55)
                / 4
                * (100 - family.calorie_discount)
                / 100,
                "protein": tdee
                * decimal.Decimal(0.15)
                / 4
                * (100 - family.calorie_discount)
                / 100,
                "fat": tdee
                * decimal.Decimal(0.30)
                / 9
                * (100 - family.calorie_discount)
                / 100,
                "fiber": tdee
                * decimal.Decimal(0.014)
                * (100 - family.calorie_discount)
                / 100,
                "sugar": tdee
                * decimal.Decimal(0.10)
                / 4
                * (100 - family.calorie_discount)
                / 100,
                "saturated_fat": tdee
                * decimal.Decimal(0.10)
                / 9
                * (100 - family.calorie_discount)
                / 100,
                "cholesterol": tdee
                * decimal.Decimal(0.10)
                * (100 - family.calorie_discount)
                / 100,
                "sodium": 1300 * (100 - family.calorie_discount) / 100,
            }
        else:
            nutrient = {
                "calorie": tdee * (100 - family.calorie_discount) / 100,
                "carbohydrate": tdee
                * decimal.Decimal(0.55)
                / 4
                * (100 - family.calorie_discount)
                / 100,
                "protein": tdee
                * decimal.Decimal(0.25)
                / 4
                * (100 - family.calorie_discount)
                / 100,
                "fat": tdee
                * decimal.Decimal(0.20)
                / 9
                * (100 - family.calorie_discount)
                / 100,
                "fiber": tdee
                * decimal.Decimal(0.014)
                * (100 - family.calorie_discount)
                / 100,
                "sugar": tdee
                * decimal.Decimal(0.10)
                / 4
                * (100 - family.calorie_discount)
                / 100,
                "saturated_fat": tdee
                * decimal.Decimal(0.10)
                / 9
                * (100 - family.calorie_discount)
                / 100,
                "cholesterol": tdee
                * decimal.Decimal(0.10)
                * (100 - family.calorie_discount)
                / 100,
                "sodium": 2300 * (100 - family.calorie_discount) / 100,
            }
        result.append(nutrient)

    result = dict(functools.reduce(operator.add, map(collections.Counter, result)))
    return result


def __calculateAge(born: datetime.date):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# endregion
