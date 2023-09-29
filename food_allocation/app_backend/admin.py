from django.contrib import admin
from django.contrib.auth.models import User
from app_backend.models.base.common_model import BaseModel
from app_backend.models.master_data.family import Family
from app_backend.models.master_data.food_restriction import FoodRestriction
from app_backend.models.master_data.person import Person
from app_backend.models.master_data.product import Product

from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.models.system_reference.storage import Storage

# Register your models here.

# region Authentication
admin.site.register(User)
# endregion

# region System References
admin.site.register(FoodCategory)
admin.site.register(Storage)
# endregion

# region Master Data
admin.site.register(Family)
admin.site.register(Product)
admin.site.register(Person)
admin.site.register(FoodRestriction)
# endregion
