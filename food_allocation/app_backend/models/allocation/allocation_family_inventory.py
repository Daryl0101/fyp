from django.db import models
from app_backend.models.base.common_model import BaseModel


class AllocationFamilyInventory(BaseModel):
    allocation_family = models.ForeignKey(
        "AllocationFamily",
        on_delete=models.PROTECT,
        related_name="allocation_family_inventories",
    )
    inventory = models.ForeignKey(
        "Inventory",
        on_delete=models.PROTECT,
        related_name="allocation_family_inventories",
    )
    quantity = models.IntegerField(default=0)
