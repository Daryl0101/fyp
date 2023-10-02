from django.urls import include, path

from app_backend.views import masterDataViews

urlpatterns = [
    # region Products
    path(
        "products/search",
        masterDataViews.productSearch,
        name="search-products",
    ),
    path(
        "products/<int:product_id>",
        masterDataViews.productDetails,
        name="view-product",
    ),
    path(
        "products/create",
        masterDataViews.productCreate,
        name="create-product",
    ),
    path(
        "products/<int:product_id>/update",
        masterDataViews.productUpdate,
        name="update-product",
    ),
    path(
        "products/<int:product_id>/delete",
        masterDataViews.productDelete,
        name="delete-product",
    ),
    # endregion
    # region Families
    path(
        "families/search",
        masterDataViews.familySearch,
        name="search-families",
    ),
    path(
        "families/<int:family_id>",
        masterDataViews.familyDetails,
        name="view-family",
    ),
    path(
        "families/create",
        masterDataViews.familyCreate,
        name="create-family",
    ),
    path(
        "families/<int:family_id>/update",
        masterDataViews.familyUpdate,
        name="update-family",
    ),
    path(
        "families/<int:family_id>/delete",
        masterDataViews.familyDelete,
        name="delete-family",
    ),
    # region Dropdown
    path(
        "families/gender/dropdown",
        masterDataViews.genderDropdown,
        name="gender-dropdown",
    ),
    path(
        "families/activity-level/dropdown",
        masterDataViews.activityLevelDropdown,
        name="activity-level-dropdown",
    ),
    # endregion
    # endregion
]
