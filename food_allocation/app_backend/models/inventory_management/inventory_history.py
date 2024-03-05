from django.db import models
from app_backend.models.base.common_model import BaseModel
from app_backend.models.inventory_management.inventory import Inventory


class InventoryHistory(BaseModel):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.PROTECT, related_name="inventory_histories"
    )
    before = models.IntegerField()
    after = models.IntegerField()
    difference = models.IntegerField()
    inventory_action = models.CharField(max_length=50)
