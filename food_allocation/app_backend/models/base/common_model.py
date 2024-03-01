from email.policy import default
import uuid
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.UUIDField(default=uuid.UUID(int=0))
    modified_by = models.UUIDField(default=uuid.UUID(int=0))

    class Meta:
        abstract = True
