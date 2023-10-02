from django.db import models
from app_backend.models.master_data.product import Product

from app_backend.models.system_reference.food_category import FoodCategory


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    food_category = models.ForeignKey(
        FoodCategory, on_delete=models.PROTECT
    )  # This is to prevent products having no food category

    class Meta:
        unique_together = ("product", "food_category")
