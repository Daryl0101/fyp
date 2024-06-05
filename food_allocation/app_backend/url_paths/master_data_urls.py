from django.urls import include, path

from app_backend.views import master_data_views

urlpatterns = [
    # region Products
    path(
        "products/search",
        master_data_views.productSearch,
        name="search-products",
    ),
    path(
        "products/<int:product_id>",
        master_data_views.productDetails,
        name="view-product",
    ),
    path(
        "products/create",
        master_data_views.productCreate,
        name="create-product",
    ),
    path(
        "products/<int:product_id>/update",
        master_data_views.productUpdate,
        name="update-product",
    ),
    path(
        "products/<int:product_id>/update-nutrition",
        master_data_views.productUpdateNutritionalInformation,
        name="update-product-nutrition",
    ),
    path(
        "products/<int:product_id>/delete",
        master_data_views.productDelete,
        name="delete-product",
    ),
    path(
        "products/ner",
        master_data_views.productNER,
        name="product-ner",
    ),
    # endregion
    # region Families
    path(
        "families/search",
        master_data_views.familySearch,
        name="search-families",
    ),
    path(
        "families/<int:family_id>",
        master_data_views.familyDetails,
        name="view-family",
    ),
    path(
        "families/create",
        master_data_views.familyCreate,
        name="create-family",
    ),
    path(
        "families/<int:family_id>/update",
        master_data_views.familyUpdate,
        name="update-family",
    ),
    path(
        "families/<int:family_id>/delete",
        master_data_views.familyDelete,
        name="delete-family",
    ),
    # region Dropdown
    path(
        "families/gender/dropdown",
        master_data_views.genderDropdown,
        name="gender-dropdown",
    ),
    path(
        "families/activity-level/dropdown",
        master_data_views.activityLevelDropdown,
        name="activity-level-dropdown",
    ),
    # endregion
    # endregion
]
