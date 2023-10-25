from django.core import validators
from django.db import models

from app_backend.enums import ActivityLevel, Gender
from app_backend.models.base.common_model import BaseModel
from app_backend.models.master_data.family import Family


class Person(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=Gender.choices)
    birthdate = models.DateField()
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    activity_level = models.IntegerField(choices=ActivityLevel.choices)
    # bmi = models.DecimalField(max_digits=10, decimal_places=2)
    # calorie = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(
        default=None, null=True, validators=[validators.URLValidator()]
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="members")
