from django.db import models

from app_backend.models.base.common_model import BaseModel


class FoodCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
