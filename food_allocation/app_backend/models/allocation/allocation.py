from django.db import models
from app_backend.enums import AllocationStatus
from app_backend.models.base.common_model import BaseModel


class Allocation(BaseModel):
    allocation_no = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)
    status = models.CharField(
        max_length=20,
        choices=AllocationStatus.choices,
        default=AllocationStatus.CREATED,
    )
    inventories = models.ManyToManyField(
        "Inventory", through="AllocationInventory", related_name="allocations"
    )
    families = models.ManyToManyField(
        "Family", through="AllocationFamily", related_name="allocations"
    )
    log = models.TextField(blank=True, default="")
    # min_product_category = models.IntegerField(default=5)
    allocation_days = models.IntegerField(default=7)
    diversification = models.IntegerField(default=5)
