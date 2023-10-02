from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import serializers
from app_backend.enums import SortOrder
from app_backend.models.system_reference.food_category import FoodCategory
from app_backend.serializers.system_reference.request.foodCategorySearchRequest import (
    FoodCategorySearchRequest,
)
from app_backend.serializers.system_reference.response.foodCategorySearchResponse import (
    FoodCategorySearchItemResponse,
    FoodCategorySearchResponse,
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
            "food_categories": FoodCategorySearchItemResponse(
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


# endregion
