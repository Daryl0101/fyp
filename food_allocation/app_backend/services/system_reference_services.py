from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import serializers
from app_backend.enums import HalalStatus, SortOrder
from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.models.system_reference.storage import Storage
from app_backend.serializers.system_reference.request.foodCategorySearchRequest import (
    FoodCategorySearchRequest,
)
from app_backend.serializers.system_reference.request.storageSearchRequest import (
    StorageSearchRequest,
)
from app_backend.serializers.system_reference.response.foodCategorySearchResponse import (
    FoodCategorySearchItemResponse,
    FoodCategorySearchResponse,
)
from app_backend.serializers.system_reference.response.storageDetailResponse import (
    StorageDetailResponse,
)
from app_backend.serializers.system_reference.response.storageSearchResponse import (
    StorageSearchItemResponse,
    StorageSearchResponse,
)
from app_backend.utils import isBlank


# region Food Categories
def retrieveFoodCategoriesByIds(ids: list[int]):
    ids = set(ids)
    if ids is None or len(ids) <= 0:
        raise serializers.ValidationError("Invalid food category ID(s)")
    foodCategories = FoodCategory.objects.filter(id__in=ids)
    if foodCategories.count() != len(ids):
        raise serializers.ValidationError("Invalid food category ID(s)")
    return foodCategories


def processSearchFoodCategories(request):
    # region Parse request
    request_parsed = FoodCategorySearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    food_categories = FoodCategory.objects.all()

    if not isBlank(request_parsed.validated_data["search_string"]):
        food_categories = food_categories.filter(
            Q(name__icontains=request_parsed.validated_data["search_string"])
            | Q(description__icontains=request_parsed.validated_data["search_string"])
        )
    # endregion

    # region Sort
    fields = FoodCategorySearchItemResponse().fields
    scso = "name"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    food_categories = food_categories.order_by(scso)
    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=food_categories,
        per_page=request_parsed.validated_data["page_size"],
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = FoodCategorySearchResponse(
        data={
            "items": FoodCategorySearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": (
                page.previous_page_number() if page.has_previous() else None
            ),
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data


# endregion


def processSearchStorages(request):
    # region Parse request
    request_parsed = StorageSearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    storages = Storage.objects.filter(is_active=True)

    if (
        request_parsed.validated_data["exclude_product_id"] is not None
        and request_parsed.validated_data["exclude_product_id"] > 0
    ):
        storages = storages.exclude(
            inventories__product_id=request_parsed.validated_data["exclude_product_id"],
            inventories__is_active=True,
        )

    if not isBlank(request_parsed.validated_data["storage_no"]):
        storages = storages.filter(
            storage_no__icontains=request_parsed.validated_data["storage_no"]
        )

    if not isBlank(request_parsed.validated_data["description"]):
        storages = storages.filter(
            description__icontains=request_parsed.validated_data["description"]
        )

    if request_parsed.validated_data["halal_status"] == HalalStatus.HALAL:
        storages = storages.filter(is_halal=True)
    elif request_parsed.validated_data["halal_status"] == HalalStatus.NON_HALAL:
        storages = storages.filter(is_halal=False)

    # endregion

    # region Sort
    fields = StorageSearchItemResponse().fields
    scso = "storage_no"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    storages = storages.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=storages, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = StorageSearchResponse(
        data={
            "items": StorageSearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": (
                page.previous_page_number() if page.has_previous() else None
            ),
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data


def processViewStorage(request, storage_id):
    inventory = retrieveActiveStorageById(id=storage_id, is_validation_required=True)
    response_serializer = StorageDetailResponse(data=inventory)

    return response_serializer.initial_data


def retrieveActiveStorageById(id: int, is_validation_required: bool):
    if id <= 0:
        raise serializers.ValidationError("Invalid Storage ID")
    storage = Storage.objects.filter(is_active=True, id=id).first()
    if is_validation_required and storage is None:
        raise serializers.ValidationError("Invalid Storage")
    return storage
