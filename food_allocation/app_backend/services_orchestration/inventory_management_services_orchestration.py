from datetime import date, datetime, time, timedelta
import os

from django.db.models import Min
from app_backend.enums import NotificationReadStatus
from app_backend.models.inventory_management.inventory import Inventory
from app_backend.services.authentication_services import retrieveNGOManagers
from app_backend.services.notification_services import addNotificationBatch


def processInformNearingExpiredInventories():
    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=7)
    # filter inventories that are expiring within 7 days
    inventories = Inventory.objects.filter(
        expiration_date__range=(start_date, end_date), is_active=True
    )
    if not inventories.exists():
        print("No near expired inventories found")
        return
    ngo_managers = retrieveNGOManagers()
    addNotificationBatch(
        [
            {
                "user_id": mng.id,
                "title": "Near expired inventories found",
                "body": f"Inventories expiring within a week: {[inventory.inventory_no for inventory in inventories]}",
                "link": f"{os.getenv('FRONTEND_BASE_URL')}/inventory?expiration_date_start={start_date.isoformat()}&expiration_date_end={end_date.isoformat()}",
                "expiry": datetime.combine(date.today(), time.max).astimezone(),
                "status": NotificationReadStatus.UNREAD,
            }
            for mng in ngo_managers
        ]
    )


def processInformExpiredInventories():
    inventories = Inventory.objects.filter(
        expiration_date__lte=date.today(), is_active=True
    )
    if not inventories.exists():
        print("No expired inventories found")
        return
    ngo_managers = retrieveNGOManagers()
    earliest_expiry: date = inventories.aggregate(Min("expiration_date"))[
        "expiration_date__min"
    ]
    addNotificationBatch(
        [
            {
                "user_id": mng.id,
                "title": "Expired inventories found",
                "body": f"Expired inventories: {[inventory.inventory_no for inventory in inventories]}",
                "link": f"{os.getenv('FRONTEND_BASE_URL')}/inventory?expiration_date_start={earliest_expiry.isoformat()}&expiration_date_end={date.today().isoformat()}",
                "expiry": datetime.combine(date.today(), time.max).astimezone(),
                "status": NotificationReadStatus.UNREAD,
            }
            for mng in ngo_managers
        ]
    )
