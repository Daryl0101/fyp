from django.urls import path

from app_backend.views import inventoryManagementViews


urlpatterns = [
    path(
        "inventories/search",
        inventoryManagementViews.inventorySearch,
        name="search-inventories",
    ),
    path(
        "inventories/<int:inventory_id>",
        inventoryManagementViews.inventoryDetails,
        name="view-inventory",
    ),
    path(
        "inventories/inbound",
        inventoryManagementViews.inventoryInbound,
        name="inbound-inventory",
    ),
    path(
        "inventories/<int:inventory_id>/adjust",
        inventoryManagementViews.inventoryAdjust,
        name="adjust-inventory",
    ),
    path(
        "inventories/<int:inventory_id>/delete",
        inventoryManagementViews.inventoryDelete,
        name="delete-inventory",
    ),
]
