from datetime import date, datetime, time, timedelta
import os

from django.db.models import Min
from app_backend.enums import NotificationReadStatus
from app_backend.models.inventory_management.inventory import Inventory
from app_backend.services.authentication_services import retrieveNGOManagers
from app_backend.services.notification_services import addNotificationBatch


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
