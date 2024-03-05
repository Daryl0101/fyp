from email.policy import default
from django.db import models

from app_backend.models.base.common_model import BaseModel
from app_backend.models.system_reference.food_category import FoodCategory


class Family(BaseModel):
    family_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(
        max_length=50
    )  # This is not unique, any family can have the same name, just identify them using the family_no
    is_halal = models.BooleanField(default=False)
    household_income = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20, blank=True)
    last_received_date = models.DateField(blank=True, null=True, default=None)
    address = models.CharField(max_length=200, blank=True)
    total_member = models.IntegerField(default=0)
    calorie_discount = models.DecimalField(max_digits=10, decimal_places=2)
    food_restrictions = models.ManyToManyField(
        FoodCategory,
        through="FoodRestriction",
        related_name="families",
    )
    is_active = models.BooleanField(default=True)
