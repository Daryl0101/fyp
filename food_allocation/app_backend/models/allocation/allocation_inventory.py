from django.db import models
from app_backend.models.base.common_model import BaseModel


class AllocationInventory(BaseModel):
    allocation = models.ForeignKey(
        "Allocation", on_delete=models.PROTECT, related_name="allocation_inventories"
    )
    inventory = models.ForeignKey(
        "Inventory", on_delete=models.PROTECT, related_name="allocation_inventories"
    )
    quantity = models.IntegerField(default=0)
    max_quantity_per_family = models.IntegerField(default=0)
