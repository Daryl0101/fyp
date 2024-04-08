from django.db import models

from app_backend.enums import PackageStatus
from app_backend.models.base.common_model import BaseModel


class Package(BaseModel):
    package_no = models.CharField(max_length=50, unique=True)
    family = models.ForeignKey(
        "Family", on_delete=models.PROTECT, related_name="packages"
    )
    allocation = models.ForeignKey(
        "Allocation", on_delete=models.PROTECT, related_name="packages"
    )
    allocation_family = models.ForeignKey(
        "AllocationFamily", on_delete=models.PROTECT, related_name="packages"
    )
    status = models.CharField(max_length=20, choices=PackageStatus.choices)
