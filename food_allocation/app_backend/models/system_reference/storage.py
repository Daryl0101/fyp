from django.db import models

from app_backend.models.base.common_model import BaseModel


class Storage(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    is_halal = models.BooleanField(default=False)
