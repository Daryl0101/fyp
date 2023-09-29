from django.db import models

from app_backend.models.base.common_model import BaseModel


class Family(BaseModel):
    family_no = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    is_halal = models.BooleanField(default=False)
    household_income = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20, blank=True)
    last_received_date = models.DateField()
    address = models.CharField(max_length=200, blank=True)
    total_member = models.IntegerField(default=0)
    calorie_discount = models.DecimalField(max_digits=10, decimal_places=2)
