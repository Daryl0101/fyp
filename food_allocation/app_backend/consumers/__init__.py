# https://blog.sneawo.com/blog/2018/12/05/how-to-split-celery-tasks-file/
from app_backend.consumers.package_consumers import PackageConsumer
from .allocation_consumers import *

__all__ = [AllocationConsumer, PackageConsumer]
