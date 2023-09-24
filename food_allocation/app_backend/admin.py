from django.contrib import admin

from app_backend.models.authentication.user import User
from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.models.system_reference.storage import Storage


# Register your models here.
admin.site.register(User)
admin.site.register(FoodCategory)
admin.site.register(Storage)
