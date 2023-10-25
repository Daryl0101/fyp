from django.core import validators
from django.db import models

from app_backend.models.base.common_model import BaseModel
from app_backend.models.system_reference.food_category import FoodCategory


class Product(BaseModel):
    product_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    image = models.URLField(
        default=None, null=True, validators=[validators.URLValidator()]
    )
    serving_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    carbohydrate_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    protein_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    fat_calorie = models.DecimalField(max_digits=10, decimal_places=2)
    is_halal = models.BooleanField(default=False)
    # total_qty = models.IntegerField(default=0)
    # available_qty = models.IntegerField(default=0)
    food_categories = models.ManyToManyField(
        FoodCategory,
        through="ProductCategory",
        related_name="products",
    )
