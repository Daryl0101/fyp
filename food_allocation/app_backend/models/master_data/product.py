# from django.db import models

# from food_allocation.app_backend.models.base.base_model import BaseModel


# class Product(BaseModel):
#     name = models.CharField(max_length=50, unique=True)
#     description = models.CharField(max_length=200, blank=True)
#     image = models.URLField(default=None, null=True)
#     serving_size = models.DecimalField(max_digits=10, decimal_places=2, )
#     carbohydrate_calorie = models.DecimalField(max_digits=10, decimal_places=2)
#     protein_calorie = models.DecimalField(max_digits=10, decimal_places=2)
#     fat_calorie = models.DecimalField(max_digits=10, decimal_places=2)
#     is_halal = models.BooleanField(default=False)
#     total_qty = models.IntegerField(default=0)
#     available_qty = models.IntegerField(default=0)
