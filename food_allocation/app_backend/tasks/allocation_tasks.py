from celery import shared_task

from app_backend.services.allocation_services import processStartAllocation


@shared_task
def taskProcessStartAllocation(allocation_id: int):
    processStartAllocation(allocation_id=allocation_id)
