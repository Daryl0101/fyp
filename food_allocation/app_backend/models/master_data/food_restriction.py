from django.db import models
from app_backend.models.base.common_model import BaseModel
from app_backend.models.master_data.family import Family

from app_backend.models.master_data.person import Person
from app_backend.models.system_reference.food_category import FoodCategory


class FoodRestriction(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    # family = models.ForeignKey(Family, on_delete=models.CASCADE)
    food_category = models.ForeignKey(
        FoodCategory, on_delete=models.PROTECT
    )  # This is to make sure all persons migrate their food restrictions to the new food category

    class Meta:
        unique_together = ("person", "food_category")
