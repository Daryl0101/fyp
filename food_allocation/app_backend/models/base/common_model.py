from email.policy import default
import uuid
from django.db import models

from app_backend.models.authentication.user import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # created_by and modified_by can be referenced to User model using foreign key because is_active is used in the User model
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")

    class Meta:
        abstract = True
