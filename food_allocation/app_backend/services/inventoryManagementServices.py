from django.core.paginator import Paginator
from app_backend.enums import HalalStatus, SortOrder
from app_backend.models.inventory_management.inventory import Inventory
from app_backend.serializers.inventory_management.request.inventorySearchRequest import (
    InventorySearchRequest,
)
from app_backend.serializers.inventory_management.response.inventorySearchResponse import (
    InventorySearchItemResponse,
    InventorySearchResponse,
)
from app_backend.services.masterDataServices import retrieveProductsByNo
from app_backend.utils import isBlank


def processSearchInventory(request):
    # region Parse request
    request_parsed = InventorySearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    inventories = Inventory.objects.all()

    if not isBlank(request_parsed.validated_data["product_no"]):
        inventories = inventories.filter(
            product__product_no__icontains=request_parsed.validated_data["product_no"]
        )

    if not isBlank(request_parsed.validated_data["product_name"]):
        inventories = inventories.filter(
            product__product_name__icontains=request_parsed.validated_data[
                "product_name"
            ]
        )

    if not isBlank(request_parsed.validated_data["storage_name"]):
        inventories = inventories.filter(
            storage__storage_name__icontains=request_parsed.validated_data[
                "storage_name"
            ]
        )

    if (
        request_parsed.validated_data["expiration_date_start"] is not None
        and request_parsed.validated_data["expiration_date_end"] is not None
    ):
        inventories = inventories.filter(
            expiration_date__range=(
                request_parsed.validated_data["expiration_date_start"],
                request_parsed.validated_data["expiration_date_end"],
            )
        )

    if not isBlank(request_parsed.validated_data["batch_no"]):
        inventories = inventories.filter(
            batch_no__icontains=request_parsed.validated_data["batch_no"]
        )

    if (
        request_parsed.validated_data["received_date_start"] is not None
        and request_parsed.validated_data["received_date_end"] is not None
    ):
        inventories = inventories.filter(
            created_at__range=(
                request_parsed.validated_data["received_date_start"],
                request_parsed.validated_data["received_date_end"],
            )
        )

    if request_parsed.validated_data["halal_status"] == HalalStatus.HALAL:
        inventories = inventories.filter(product__is_halal=True)
    elif request_parsed.validated_data["halal_status"] == HalalStatus.NON_HALAL:
        inventories = inventories.filter(product__is_halal=False)
    # endregion

    # region Sort
    fields = InventorySearchItemResponse().fields
    scso = "expiration_date"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    inventories = inventories.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=inventories, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = InventorySearchResponse(
        data={
            "products": InventorySearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": page.previous_page_number()
            if page.has_previous()
            else None,
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data
