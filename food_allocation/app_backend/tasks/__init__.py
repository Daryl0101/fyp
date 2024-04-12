# https://blog.sneawo.com/blog/2018/12/05/how-to-split-celery-tasks-file/
from app_backend.tasks.allocation_tasks import taskProcessStartAllocation
from app_backend.tasks.daily_tasks import (
    taskProcessCancelExpiredPackages,
    taskProcessInformExpiredInventories,
    taskProcessRejectExpiredAllocationFamilies,
    taskProcessRemoveExpiredNotifications,
)

__all__ = [
    taskProcessStartAllocation,
    taskProcessRejectExpiredAllocationFamilies,
    taskProcessCancelExpiredPackages,
    taskProcessInformExpiredInventories,
    taskProcessRemoveExpiredNotifications,
]
