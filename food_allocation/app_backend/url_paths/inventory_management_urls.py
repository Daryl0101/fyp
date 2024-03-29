from django.urls import path

from app_backend.views import inventory_management_views


urlpatterns = [
    path(
        "inventories/search",
        inventory_management_views.inventorySearch,
        name="search-inventories",
    ),
    path(
        "inventories/<int:inventory_id>",
        inventory_management_views.inventoryDetails,
        name="view-inventory",
    ),
    path(
        "inventories/inbound",
        inventory_management_views.inventoryInbound,
        name="inbound-inventory",
    ),
    path(
        "inventories/<int:inventory_id>/adjust",
        inventory_management_views.inventoryAdjust,
        name="adjust-inventory",
    ),
    path(
        "inventories/<int:inventory_id>/delete",
        inventory_management_views.inventoryDelete,
        name="delete-inventory",
    ),
]
