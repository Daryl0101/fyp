from email.policy import default
from django.db import models
from app_backend.enums import InventoryMovement
from app_backend.models.base.common_model import BaseModel
from app_backend.models.inventory_management.inventory import Inventory


class InventoryHistory(BaseModel):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.PROTECT, related_name="inventory_histories"
    )
    before = models.IntegerField()
    after = models.IntegerField()
    difference = models.IntegerField()
    movement = models.CharField(max_length=50, choices=InventoryMovement.choices)
    reason = models.CharField(max_length=200, blank=True, default="")
