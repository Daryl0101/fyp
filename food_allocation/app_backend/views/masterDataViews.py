from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
    ProductSearchResponse,
)
from app_backend.services.masterDataServices import (
    processCreateProduct,
    processDeleteProduct,
    processSearchProducts,
    processUpdateProduct,
    processViewProduct,
)
from app_backend.utils import baseResponseSerializerGenerator
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from app_backend.decorators import response_handler


# region Products
@extend_schema(
    parameters=[ProductSearchRequest],
    responses={
        200: baseResponseSerializerGenerator(
            model=ProductSearchResponse(allow_null=True)
        )
    },
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=ProductSearchResponse(allow_null=True))
def productSearch(request):
    return processSearchProducts(request)


@extend_schema(
    responses={
        200: baseResponseSerializerGenerator(
            model=ProductDetailResponse(allow_null=True)
        )
    },
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=ProductDetailResponse(allow_null=True))
def productDetails(request, product_id):
    return processViewProduct(request, product_id)


@extend_schema(
    request=ProductCreateUpdateRequest,
    responses={
        200: baseResponseSerializerGenerator(
            model=serializers.BooleanField(allow_null=True)
        )
    },
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productCreate(request):
    return processCreateProduct(request)


@extend_schema(
    request=ProductCreateUpdateRequest,
    responses={
        200: baseResponseSerializerGenerator(
            model=serializers.BooleanField(allow_null=True)
        )
    },
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productUpdate(request, product_id):
    return processUpdateProduct(request, product_id)


@extend_schema(
    responses={
        200: baseResponseSerializerGenerator(
            model=serializers.BooleanField(allow_null=True)
        )
    },
)
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productDelete(request, product_id):
    return processDeleteProduct(request, product_id)


# endregion

# class MasterDataViews(viewsets.GenericViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     # region Products
#     @extend_schema(
#         parameters=[ProductSearchRequest],
#         responses={
#             200: baseResponseSerializerGenerator(
#                 model=ProductSearchResponse(allow_null=True)
#             )
#         },
#     )
#     @action(
#         methods=["GET"],
#         url_path="products/search",
#         detail=False,
#     )
#     @response_handler(responses=ProductSearchResponse(allow_null=True))
#     def productSearch(self, request):
#         return processSearchProducts(request)

#     @extend_schema(
#         responses={
#             200: baseResponseSerializerGenerator(
#                 model=ProductDetailResponse(allow_null=True)
#             )
#         },
#     )
#     @action(
#         methods=["GET"],
#         url_path="products/(?P<product_id>\d+)",
#         detail=False,
#     )
#     @response_handler(responses=ProductDetailResponse(allow_null=True))
#     def productDetails(self, request, product_id):
#         return processViewProduct(request, product_id)

#     # endregion
