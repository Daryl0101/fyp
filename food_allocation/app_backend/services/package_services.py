from __future__ import annotations
from typing import TYPE_CHECKING

from app_backend.models.authentication.user import User
from app_backend.models.package.package_history import PackageHistory
from app_backend.models.package.package_item import PackageItem
from app_backend.utils import generateItemNoFromId, setCreateUpdateProperty

if TYPE_CHECKING:
    from app_backend.models.allocation.allocation_family import AllocationFamily
    from app_backend.models.master_data.family import Family
from app_backend.enums import ActionType, ItemNoPrefix, PackageStatus
from app_backend.models.package.package import Package


def createPackageByAllocationFamily(
    allocation_family: AllocationFamily, user: User
) -> Package:
    package = Package(
        family=allocation_family.family,
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


def createPackageHistory(package: Package, user: User) -> None:
    package_history = PackageHistory(package=package, action=package.status)
    setCreateUpdateProperty(
        model=package_history, userObject=user, actionType=ActionType.CREATE
    )
    package_history.save()
