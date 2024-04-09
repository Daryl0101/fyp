from celery import shared_task
from app_backend.services.allocation_services import (
    processRejectExpiredAllocationFamilies,
)
from app_backend.services.package_services import processCancelExpiredPackages


@shared_task
def taskProcessRejectExpiredAllocationFamilies():
    processRejectExpiredAllocationFamilies()


@shared_task
def taskProcessCancelExpiredPackages():
    processCancelExpiredPackages()
