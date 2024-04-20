from datetime import date, datetime, time
import os
from django.db import transaction
from channels.consumer import get_channel_layer
from channels.generic.websocket import async_to_sync
from app_backend.enums import (
    ActionType,
    AllocationFamilyStatus,
    AllocationStatus,
    NotificationReadStatus,
)
from app_backend.models.allocation.allocation_family import AllocationFamily
from app_backend.services.authentication_services import retrieveNGOManagers
from app_backend.services.notification_services import addNotificationBatch
from app_backend.utils import setCreateUpdateProperty


def processRejectExpiredAllocationFamilies():
    # retrieve all allocation families with status SERVED and expired inventories
    allocation_families = AllocationFamily.objects.filter(
        status=AllocationFamilyStatus.SERVED,
        inventories__expiration_date__lte=date.today(),
    )
    if not allocation_families.exists():
        return
    current_allocation = allocation_families.first().allocation
    with transaction.atomic():
        for af in allocation_families:
            # update allocation_family status to STATUS.REJECTED, save
            af.status = AllocationFamilyStatus.REJECTED
            setCreateUpdateProperty(af, af.created_by, ActionType.UPDATE)
            # TODO: create a separate account for the system, to differentiate system actions from user actions
            af.save()
            # update allocation status to AllocationStatus.COMPLETED if allocation_family is the last accepted family, save
        if (
            current_allocation.allocation_families.filter(
                status__in=[
                    AllocationFamilyStatus.ACCEPTED,
                    AllocationFamilyStatus.REJECTED,
                    AllocationFamilyStatus.NOT_SERVED,
                ]
            ).count()
            == current_allocation.allocation_families.count()
        ):
            current_allocation.status = AllocationStatus.COMPLETED
            setCreateUpdateProperty(
                current_allocation, current_allocation.created_by, ActionType.UPDATE
            )
            current_allocation.save()

    ngo_managers = retrieveNGOManagers()
    channel_layer = get_channel_layer()
    if (
        current_allocation.allocation_families.filter(
            status__in=[
                AllocationFamilyStatus.ACCEPTED,
                AllocationFamilyStatus.REJECTED,
                AllocationFamilyStatus.NOT_SERVED,
            ]
        ).count()
        == current_allocation.allocation_families.count()
    ):
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
    addNotificationBatch(
        [
            {
                "user_id": mng.id,
                "title": "Expired Inventories in Allocation Families",
                "body": f"Families with rejected allocation: {[allocation_family.family.family_no for allocation_family in allocation_families]}",
                "link": f"{os.getenv('FRONTEND_BASE_URL')}/allocation",
                "expiry": datetime.combine(date.today(), time.max).astimezone(),
                "status": NotificationReadStatus.UNREAD,
            }
            for mng in ngo_managers
        ]
    )
    # print(
    #     "Expired allocation families have been rejected - Allocation not completed"
    # )
