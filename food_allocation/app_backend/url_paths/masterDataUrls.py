from django.urls import path

from app_backend.views import masterDataViews


urlpatterns = [
    path("products/search", masterDataViews.productSearch, name="search-products"),
    path(
        "products/<int:product_id>",
        masterDataViews.productDetails,
        name="create-product",
    ),
    path("products/create", masterDataViews.productCreate, name="create-product"),
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
]
