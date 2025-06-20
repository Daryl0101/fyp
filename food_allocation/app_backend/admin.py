from django.contrib import admin
from app_backend.models.allocation.allocation import Allocation
from app_backend.models.allocation.allocation_family import AllocationFamily
from app_backend.models.allocation.allocation_family_inventory import (
    AllocationFamilyInventory,
)
from app_backend.models.allocation.allocation_inventory import AllocationInventory
from app_backend.models.authentication.user import User
from app_backend.models.inventory_management.inventory import Inventory
from app_backend.models.inventory_management.inventory_history import InventoryHistory
from app_backend.models.master_data.family import Family
from app_backend.models.master_data.food_restriction import FoodRestriction
from app_backend.models.master_data.person import Person
from app_backend.models.master_data.product import Product
from app_backend.models.master_data.product_category import ProductCategory

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
admin.site.register(ProductCategory)
# endregion

# region Inventory Management
admin.site.register(Inventory)
admin.site.register(InventoryHistory)
# endregion

# region Allocation
admin.site.register(Allocation)
admin.site.register(AllocationInventory)
admin.site.register(AllocationFamily)
admin.site.register(AllocationFamilyInventory)
# endregion
