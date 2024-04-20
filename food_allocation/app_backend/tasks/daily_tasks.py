from celery import shared_task
from app_backend.services.notification_services import removeExpiredNotificationBatch
from app_backend.services_orchestration.allocation.daily_allocation_service_orchestration import (
    processRejectExpiredAllocationFamilies,
)
from app_backend.services_orchestration.inventory_management_services_orchestration import (
    processInformExpiredInventories,
)
from app_backend.services_orchestration.package_services_orchestration import (
    processCancelExpiredPackages,
)


@shared_task
def taskProcessRejectExpiredAllocationFamilies():
    processRejectExpiredAllocationFamilies()


@shared_task
def taskProcessCancelExpiredPackages():
    processCancelExpiredPackages()


@shared_task
def taskProcessInformExpiredInventories():
    processInformExpiredInventories()


@shared_task
def taskProcessRemoveExpiredNotifications():
    removeExpiredNotificationBatch()
