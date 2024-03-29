from django.urls import path
from app_backend.views import allocation_views

urlpatterns = [
    path(
        "search",
        allocation_views.allocationSearch,
        name="search-allocations",
    ),
    path(
        "<int:allocation_id>",
        allocation_views.allocationDetails,
        name="view-allocation",
    ),
    path("create", allocation_views.allocationCreate, name="create-allocation"),
    path(
        "creatable",
        allocation_views.allocationValidateCreateIsAllowed,
        name="creatable",
    ),
    path(
        "family/search",
        allocation_views.allocationFamilySearch,
        name="search-allocation-families",
    ),
    path(
        "inventory/search",
        allocation_views.allocationInventorySearch,
        name="search-allocation-inventories",
    ),
    path(
        "family/<int:allocation_family_id>/accept",
        allocation_views.allocationFamilyAccept,
        name="accept-allocation-family",
    ),
    path(
        "family/<int:allocation_family_id>/reject",
        allocation_views.allocationFamilyReject,
        name="reject-allocation-family",
    ),
]
