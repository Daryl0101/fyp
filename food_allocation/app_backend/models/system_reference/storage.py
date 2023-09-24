from django.db import models

from app_backend.models.base.common_model import CommonModel


class Storage(models.Model, CommonModel):
    name = models.CharField(max_length=50, unique=True)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
