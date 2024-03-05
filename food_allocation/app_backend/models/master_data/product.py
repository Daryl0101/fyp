from django.core import validators
from django.db import models

from app_backend.models.base.common_model import BaseModel
from app_backend.models.system_reference.food_category import FoodCategory


class Product(BaseModel):
    product_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(
        max_length=50
    )  # This field is unique, but unique=True is not set because it is not unique in the database due to the is_active field
    description = models.CharField(max_length=200, blank=True)
    image = models.URLField(
        default=None,
        null=True,
        # , validators=[validators.URLValidator()]
    )
    serving_size = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    calorie = models.DecimalField(max_digits=10, decimal_places=2)  # kcal
    carbohydrate = models.DecimalField(max_digits=10, decimal_places=2)  # g
    protein = models.DecimalField(max_digits=10, decimal_places=2)  # g
    fat = models.DecimalField(max_digits=10, decimal_places=2)  # g
    fiber = models.DecimalField(max_digits=10, decimal_places=2)  # g
    sugar = models.DecimalField(max_digits=10, decimal_places=2)  # g
    saturated_fat = models.DecimalField(max_digits=10, decimal_places=2)  # g
    cholesterol = models.DecimalField(max_digits=10, decimal_places=2)  # mg
    sodium = models.DecimalField(max_digits=10, decimal_places=2)  # mg
    is_halal = models.BooleanField(default=False)
    # total_qty = models.IntegerField(default=0)
    # available_qty = models.IntegerField(default=0)
    food_categories = models.ManyToManyField(
        FoodCategory,
        through="ProductCategory",
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
