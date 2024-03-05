from django.db import models

from app_backend.models.base.common_model import BaseModel


class Storage(BaseModel):
    storage_no = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    is_halal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
