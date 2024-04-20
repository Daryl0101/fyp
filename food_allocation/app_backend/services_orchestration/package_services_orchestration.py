from datetime import date, datetime, time
import os

from channels.consumer import async_to_sync, get_channel_layer
from django.db import transaction

from app_backend.enums import ActionType, NotificationReadStatus, PackageStatus
from app_backend.models.package.package import Package
from app_backend.services.authentication_services import retrieveNGOManagers
from app_backend.services.notification_services import addNotificationBatch
from app_backend.services.package_services import createPackageHistory
from app_backend.utils import setCreateUpdateProperty


def processCancelExpiredPackages():
    packages = Package.objects.filter(
        status__in=[PackageStatus.NEW, PackageStatus.PACKED],
        package_items__inventory__expiration_date__lte=date.today(),
    )
    if not packages.exists():
        return
    with transaction.atomic():
        for package in packages:
            if package.status == PackageStatus.NEW:
                # package_items = PackageItem.objects.filter(package=package)
                package_items = package.package_items.all()
                for package_item in package_items:
                    package_item.inventory.available_qty += package_item.quantity
                    setCreateUpdateProperty(
                        model=package_item.inventory,
                        userObject=package.created_by,
                        actionType=ActionType.UPDATE,
                    )
                    package_item.inventory.save()
            package.status = PackageStatus.CANCELLED
            setCreateUpdateProperty(
                model=package,
                userObject=package.created_by,
                actionType=ActionType.UPDATE,
            )
            package.save()
            createPackageHistory(
                package, package.created_by, "Expired inventory in package"
            )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "package",
        {
            "type": "package_state_update",
            "message": [str(package.id) for package in packages],
        },
    )

    ngo_managers = retrieveNGOManagers()

    addNotificationBatch(
        [
            {
                "id": mng.id,
                "title": "Expired Inventories in Packages",
                "body": f"Rejected Packages: {[package.package_no for package in packages]}",
                "link": f"{os.getenv('FRONTEND_BASE_URL')}/package",
                "expiry": datetime.combine(date.today(), time.max).astimezone(),
                "status": NotificationReadStatus.UNREAD,
            }
            for mng in ngo_managers
        ]
    )
