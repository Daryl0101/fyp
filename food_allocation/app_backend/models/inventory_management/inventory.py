from django.db import models
from app_backend.models.base.common_model import BaseModel
from app_backend.models.master_data.product import Product
from app_backend.models.system_reference.storage import Storage


class Inventory(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventories"
    )  # To ensure inventory does not contain the product before deleting a product
    storage = models.ForeignKey(
        Storage, on_delete=models.PROTECT, related_name="inventories"
    )  # To ensure all products are moved to another storage before deleting a storage
    serving_size = models.DecimalField(default=1, decimal_places=2, max_digits=10)
    carbohydrate_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    protein_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    fat_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField()
    batch_no = models.CharField(max_length=50)
    total_qty = models.IntegerField(default=1)
    available_qty = models.IntegerField(default=0)
