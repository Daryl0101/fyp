from __future__ import annotations
from typing import TYPE_CHECKING

from channels.consumer import async_to_sync, get_channel_layer
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import serializers

from app_backend.models.authentication.user import User
from app_backend.models.package.package_history import PackageHistory
from app_backend.models.package.package_item import PackageItem
from app_backend.serializers.package.request.packageSearchRequest import (
    PackageSearchRequest,
)
from app_backend.serializers.package.response.packageDetailResponse import (
    PackageDetailResponse,
)
from app_backend.serializers.package.response.packageSearchResponse import (
    PackageSearchItemResponse,
    PackageSearchResponse,
)
from app_backend.services.inventory_management_services import createInventoryHistory
from app_backend.utils import generateItemNoFromId, isBlank, setCreateUpdateProperty

if TYPE_CHECKING:
    from app_backend.models.allocation.allocation_family import AllocationFamily
    from app_backend.models.master_data.family import Family
from app_backend.enums import (
    ActionType,
    InventoryMovement,
    ItemNoPrefix,
    PackageStatus,
    SortOrder,
)
from app_backend.models.package.package import Package
from datetime import date, datetime


def processSearchPackages(request):
    # region Parse request
    request_parsed = PackageSearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    packages = Package.objects.all()

    if not isBlank(request_parsed.validated_data["package_no"]):
        packages = packages.filter(
            package_no__icontains=request_parsed.validated_data["package_no"]
        )

    if not isBlank(request_parsed.validated_data["family_no"]):
        packages = packages.filter(
            family__family_no__icontains=request_parsed.validated_data["family_no"]
        )

    if not isBlank(request_parsed.validated_data["allocation_no"]):
        packages = packages.filter(
            allocation__allocation_no__icontains=request_parsed.validated_data[
                "allocation_no"
            ]
        )

    if not isBlank(request_parsed.validated_data["inventory_no"]):
        packages = packages.filter(
            package_items__inventory__inventory_no__icontains=request_parsed.validated_data[
                "inventory_no"
            ]
        )

    if not isBlank(request_parsed.validated_data["product_no"]):
        packages = packages.filter(
            package_items__inventory__product__product_no__icontains=request_parsed.validated_data[
                "product_no"
            ]
        )

    if not isBlank(request_parsed.validated_data["product_name"]):
        packages = packages.filter(
            package_items__inventory__product__name__icontains=request_parsed.validated_data[
                "product_name"
            ]
        )

    if not isBlank(request_parsed.validated_data["status"]):
        packages = packages.filter(status=request_parsed.validated_data["status"])

    # endregion

    # region Sort
    fields = PackageSearchItemResponse().fields
    scso = "modified_at"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    packages = packages.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=packages, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = PackageSearchResponse(
        data={
            "items": PackageSearchItemResponse(
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


def processViewPackage(request, package_id):
    if int(package_id) < 0:
        raise serializers.ValidationError("Invalid Package ID")
    package = Package.objects.filter(id=package_id).first()
    if package is None:
        raise serializers.ValidationError("Invalid Package")
    response_serializer = PackageDetailResponse(data=package)
    return response_serializer.initial_data


def processPackPackage(request, package_id):
    result = False

    with transaction.atomic():
        if int(package_id) < 0:
            raise serializers.ValidationError("Invalid Package ID")

        package = Package.objects.filter(
            id=package_id, status=PackageStatus.NEW
        ).first()
        if package is None:
            raise serializers.ValidationError("Invalid Package")

        # package_items = PackageItem.objects.filter(package=package)
        package_items = package.package_items.all()
        for package_item in package_items:
            if package_item.inventory.is_active == False:
                raise serializers.ValidationError(
                    package_item.inventory.inventory_no
                    + " has been completely used up or removed from inventory"
                )
            if package_item.inventory.total_qty < package_item.quantity:
                raise serializers.ValidationError(
                    "Insufficient quantity for "
                    + package_item.inventory.inventory_no
                    + " in "
                    + package.package_no
                )
            if package_item.inventory.expiration_date <= date.today():
                raise serializers.ValidationError(
                    "Product: "
                    + package_item.inventory.product.name
                    + " in package: "
                    + package.package_no
                    + " has expired"
                )
            before = package_item.inventory.total_qty
            package_item.inventory.total_qty -= package_item.quantity
            if package_item.inventory.total_qty == 0:
                package_item.inventory.is_active = False
            setCreateUpdateProperty(
                model=package_item.inventory,
                userObject=request.user,
                actionType=ActionType.UPDATE,
            )
            package_item.inventory.save()
            createInventoryHistory(
                inventory=package_item.inventory,
                user=request.user,
                before=before,
                after=package_item.inventory.total_qty,
                movement=InventoryMovement.OUTBOUND,
                reason="Packed in package: " + package.package_no,
            )

        package.status = PackageStatus.PACKED
        setCreateUpdateProperty(
            actionType=ActionType.UPDATE, model=package, userObject=request.user
        )
        package.save()
        createPackageHistory(package, request.user)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "package",
        {
            "type": "package_state_update",
            "message": [str(package_id)],
        },
    )

    result = True
    return result


def processDeliverPackage(request, package_id):
    result = False

    with transaction.atomic():
        if int(package_id) < 0:
            raise serializers.ValidationError("Invalid Package ID")

        package = Package.objects.filter(
            id=package_id, status=PackageStatus.PACKED
        ).first()
        if package is None:
            raise serializers.ValidationError("Invalid Package")

        # package_items = PackageItem.objects.filter(package=package)
        package_items = package.package_items.all()
        for package_item in package_items:
            if package_item.inventory.expiration_date <= date.today():
                raise serializers.ValidationError(
                    "Product: "
                    + package_item.inventory.product.name
                    + " in package: "
                    + package.package_no
                    + " has expired, please cancel the package"
                )

        package.family.last_received_date = date.today()
        package.family.save()

        package.status = PackageStatus.DELIVERED
        setCreateUpdateProperty(
            actionType=ActionType.UPDATE, model=package, userObject=request.user
        )
        package.save()
        createPackageHistory(package, request.user)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "package",
        {
            "type": "package_state_update",
            "message": [str(package_id)],
        },
    )

    result = True
    return result


def processCancelPackage(request, package_id):
    result = False

    with transaction.atomic():
        if int(package_id) < 0:
            raise serializers.ValidationError("Invalid Package ID")

        cancel_reason = request.data.get("cancel_reason")
        if isBlank(cancel_reason):
            raise serializers.ValidationError("Cancel Reason is required")

        package = Package.objects.filter(
            id=package_id, status__in=[PackageStatus.NEW, PackageStatus.PACKED]
        ).first()
        if package is None:
            raise serializers.ValidationError("Invalid Package")

        if package.status == PackageStatus.NEW:
            # package_items = PackageItem.objects.filter(package=package)
            package_items = package.package_items.all()
            for package_item in package_items:
                package_item.inventory.available_qty += package_item.quantity
                setCreateUpdateProperty(
                    model=package_item.inventory,
                    userObject=request.user,
                    actionType=ActionType.UPDATE,
                )
                package_item.inventory.save()

        package.status = PackageStatus.CANCELLED
        setCreateUpdateProperty(
            model=package, userObject=request.user, actionType=ActionType.UPDATE
        )
        package.save()
        createPackageHistory(package, request.user, cancel_reason)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "package",
        {
            "type": "package_state_update",
            "message": [str(package_id)],
        },
    )

    result = True
    return result


# region Called by other services
def createPackageByAllocationFamily(
    allocation_family: AllocationFamily, user: User
) -> Package:
    package = Package(
        family=allocation_family.family,
        allocation=allocation_family.allocation,
        allocation_family=allocation_family,
        status=PackageStatus.NEW,
    )
    setCreateUpdateProperty(
        model=package, userObject=user, actionType=ActionType.CREATE
    )
    package.save()
    package.package_no = generateItemNoFromId(
        prefix=ItemNoPrefix.PACKAGE, id=package.id
    )
    package.save()
    for (
        allocation_family_inventory
    ) in allocation_family.allocation_family_inventories.all():
        package_item = PackageItem(
            package=package,
            inventory=allocation_family_inventory.inventory,
            quantity=allocation_family_inventory.quantity,
        )
        package_item.save()
        allocation_family_inventory.inventory.available_qty -= (
            allocation_family_inventory.quantity
        )
        allocation_family_inventory.inventory.save()
    createPackageHistory(package, user)
    return package


def createPackageHistory(package: Package, user: User, cancel_reason: str = "") -> None:
    package_history = PackageHistory(package=package, action=package.status)
    if package.status == PackageStatus.CANCELLED and not isBlank(cancel_reason):
        package_history.cancel_reason = cancel_reason
    setCreateUpdateProperty(
        model=package_history, userObject=user, actionType=ActionType.CREATE
    )
    package_history.save()


# endregion
