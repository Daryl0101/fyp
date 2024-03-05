from django.db import models
from app_backend.models.base.common_model import BaseModel
from app_backend.models.master_data.product import Product
from app_backend.models.system_reference.storage import Storage


class Inventory(BaseModel):
    inventory_no = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventories"
    )  # To ensure inventory does not contain the product before deleting a product
    storage = models.ForeignKey(
        Storage, on_delete=models.PROTECT, related_name="inventories"
    )  # To ensure all products are moved to another storage before deleting a storage
    expiration_date = models.DateField()
    received_date = models.DateField()
    total_qty = models.IntegerField()
    available_qty = models.IntegerField()
    num_of_serving = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)
