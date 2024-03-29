from django.db import models

from app_backend.models.base.common_model import BaseModel


# By right, this should have is_active field, but it is not implemented as this will seldom change
# Therefore, this is a static data, delete this record only if it is not used in any other records
# When deleting a food category used in other records, it will throw a on_delete=PROTECT error
class FoodCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
