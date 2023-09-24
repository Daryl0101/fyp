from django.db import models

from app_backend.models.base.common_model import CommonModel


class FoodCategory(models.Model, CommonModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
