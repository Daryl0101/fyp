import uuid
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.UUIDField()
    modified_by = models.UUIDField()

    class Meta:
        abstract = True
