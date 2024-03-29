from django.db import models
from app_backend.enums import AllocationFamilyStatus
from app_backend.models.base.common_model import BaseModel


class AllocationFamily(BaseModel):
    allocation = models.ForeignKey(
        "Allocation", on_delete=models.PROTECT, related_name="allocation_families"
    )
    family = models.ForeignKey(
        "Family", on_delete=models.PROTECT, related_name="allocation_families"
    )
    inventories = models.ManyToManyField(
        "Inventory",
        through="AllocationFamilyInventory",
        related_name="allocation_families",
    )
    status = models.CharField(
        max_length=20,
        choices=AllocationFamilyStatus.choices,
        default=AllocationFamilyStatus.PENDING,
    )
    calorie_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    carbohydrate_needed = models.DecimalField(
        decimal_places=2, max_digits=10, default=0
    )
    protein_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fat_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fiber_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    sugar_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    saturated_fat_needed = models.DecimalField(
        decimal_places=2, max_digits=10, default=0
    )
    cholesterol_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    sodium_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    calorie_allocated = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    carbohydrate_allocated = models.DecimalField(
        decimal_places=2, max_digits=10, default=0
    )
    protein_allocated = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fat_allocated = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fiber_allocated = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    sugar_allocated = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    saturated_fat_allocated = models.DecimalField(
        decimal_places=2, max_digits=10, default=0
    )
    cholesterol_allocated = models.DecimalField(
        decimal_places=2, max_digits=10, default=0
    )
    sodium_allocated = models.DecimalField(decimal_places=2, max_digits=10, default=0)
