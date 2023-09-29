from django.core import validators
from django.db import models

from app_backend.enums import ActivityLevel, Gender
from app_backend.models.base.common_model import BaseModel
from app_backend.models.master_data.family import Family
from app_backend.models.system_reference.food_category import FoodCategory


class Person(BaseModel):
    first_name = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50, unique=True)
    gender = models.CharField(choices=Gender.choices)
    birthdate = models.DateField()
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    activity_level = models.CharField(choices=ActivityLevel.choices)
    bmi = models.DecimalField(max_digits=10, decimal_places=2)
    calorie = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(
        default=None, null=True, validators=[validators.URLValidator()]
    )
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    food_restrictions = models.ManyToManyField(
        FoodCategory,
        through="FoodRestriction",
        through_fields=("person", "food_category"),
    )
