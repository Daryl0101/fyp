from django.core.paginator import Paginator
from django.db.models import Q
from django.db.transaction import atomic
from rest_framework import serializers
from app_backend.enums import ActionType, HalalStatus
from app_backend.models.master_data.product import Product
from app_backend.serializers.master_data.request.productCreateRequest import (
    ProductCreateUpdateRequest,
)
from app_backend.serializers.master_data.request.productSearchRequest import (
    ProductSearchRequest,
)
from app_backend.serializers.master_data.response.productDetailResponse import (
    ProductDetailResponse,
)
from app_backend.serializers.master_data.response.productSearchResponse import (
    ProductSearchItemResponse,
    ProductSearchResponse,
)
from app_backend.utils import isBlank, setCreateUpdateProperty


# region Products
def processSearchProducts(request):
    # region Parse request
    request_parsed = ProductSearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter products
    products = Product.objects.all()

    if not isBlank(request_parsed.validated_data["product_no"]):
        products = products.filter(
            product_no__icontains=request_parsed.validated_data["product_no"]
        )

    if not isBlank(request_parsed.validated_data["product_name_or_description"]):
        products = products.filter(
            Q(
                name__icontains=request_parsed.validated_data[
                    "product_name_or_description"
                ]
            )
            | Q(
                description__icontains=request_parsed.validated_data[
                    "product_name_or_description"
                ]
            )
        )

    if request_parsed.validated_data["halal_status"] is HalalStatus.HALAL:
        products = products.filter(is_halal=True)

    if request_parsed.validated_data["halal_status"] is HalalStatus.NON_HALAL:
        products = products.filter(is_halal=False)
    # endregion

    # region Sort products
    fields = ProductSearchItemResponse().fields
    if not request_parsed.validated_data["sort_column"] in fields.keys():
        products = products.order_by("modified_at")
    else:
        products = products.order_by(request_parsed.validated_data["sort_column"])

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=products, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = ProductSearchResponse(
        data={
            "products": ProductSearchItemResponse(
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


def processViewProduct(request, product_id):
    if int(product_id) <= 0:
        raise serializers.ValidationError("Invalid Product ID")
    product = Product.objects.filter(id=product_id).first()
    if product is None:
        raise serializers.ValidationError("Invalid Product")
    response_serializer = ProductDetailResponse(data=product)
    return response_serializer.initial_data


@atomic
def processCreateProduct(request):
    result = False

    request_parsed = ProductCreateUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    product = Product(
        name=request_parsed.validated_data["name"],
        description=request_parsed.validated_data["description"],
        serving_size=request_parsed.validated_data["serving_size"],
        carbohydrate_calorie=request_parsed.validated_data["carbs_calorie"],
        protein_calorie=request_parsed.validated_data["protein_calorie"],
        fat_calorie=request_parsed.validated_data["fat_calorie"],
        is_halal=request_parsed.validated_data["is_halal"],
    )
    setCreateUpdateProperty(product, request.user, ActionType.CREATE)
    product.save()

    product.product_no = "P" + str(product.id).zfill(5)
    product.save()

    result = True

    return result


def processUpdateProduct(request, product_id):
    result = False

    if product_id <= 0:
        raise serializers.ValidationError("Invalid Product ID")

    request_parsed = ProductCreateUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    product = Product.objects.filter(id=product_id).first()
    if product is None:
        raise serializers.ValidationError("Invalid Product")

    product.name = request_parsed.validated_data["name"]
    product.description = request_parsed.validated_data["description"]
    product.serving_size = request_parsed.validated_data["serving_size"]
    product.carbohydrate_calorie = request_parsed.validated_data["carbs_calorie"]
    product.protein_calorie = request_parsed.validated_data["protein_calorie"]
    product.fat_calorie = request_parsed.validated_data["fat_calorie"]
    product.is_halal = request_parsed.validated_data["is_halal"]
    setCreateUpdateProperty(product, request.user, ActionType.UPDATE)
    product.save()

    result = True

    return result


def processDeleteProduct(request, product_id):
    result = False

    if product_id <= 0:
        raise serializers.ValidationError("Invalid Product ID")
    product = Product.objects.filter(id=product_id).first()
    if product is None:
        raise serializers.ValidationError("Invalid Product")
    product.delete()

    result = True

    return result


# endregion

# region Families

# endregion
