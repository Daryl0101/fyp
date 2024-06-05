from django.http.multipartparser import MultiPartParser
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app_backend.serializers.master_data.request.familyCreateUpdateRequest import (
    FamilyCreateUpdateRequest,
)
from app_backend.serializers.master_data.request.familySearchRequest import (
    FamilySearchRequest,
)
from app_backend.serializers.master_data.request.productCreateUpdateRequest import (
    ProductCreateUpdateRequest,
)
from app_backend.serializers.master_data.request.productNutritionalInformationNERRequest import (
    ProductNutritionalInformationNERRequest,
)
from app_backend.serializers.master_data.request.productSearchRequest import (
    ProductSearchRequest,
)
from app_backend.serializers.master_data.request.productUpdateRequest import (
    ProductUpdateRequest,
)
from app_backend.serializers.master_data.response.activityLevelDropdownResponse import (
    ActivityLevelDropdownResponse,
)
from app_backend.serializers.master_data.response.familyDetailResponse import (
    FamilyDetailResponse,
)
from app_backend.serializers.master_data.response.familySearchResponse import (
    FamilySearchResponse,
)
from app_backend.serializers.master_data.response.genderDropdownResponse import (
    GenderDropdownResponse,
)
from app_backend.serializers.master_data.response.productDetailResponse import (
    ProductDetailResponse,
)
from app_backend.serializers.master_data.response.productNutritionalInformationNERResponse import (
    ProductNutritionalInformationNERResponse,
)
from app_backend.serializers.master_data.response.productSearchResponse import (
    ProductSearchResponse,
)
from app_backend.services.master_data_services import (
    processCreateFamily,
    processCreateProduct,
    processDeleteFamily,
    processDeleteProduct,
    processProductNutritionalInformationNER,
    processRetrieveActivityLevelDropdown,
    processRetrieveGenderDropdown,
    processSearchFamilies,
    processSearchProducts,
    processUpdateFamily,
    processUpdateProduct,
    processUpdateProductNutritionalInformation,
    processViewFamily,
    processViewProduct,
)
from app_backend.utils import schemaWrapper
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    parser_classes,
    permission_classes,
)
from app_backend.decorators import response_handler


# region Products
@extend_schema(
    parameters=[ProductSearchRequest],
    responses={200: schemaWrapper(ProductSearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=ProductSearchResponse(allow_null=True))
def productSearch(request):
    return processSearchProducts(request)


@extend_schema(
    responses={200: schemaWrapper(ProductDetailResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=ProductDetailResponse(allow_null=True))
def productDetails(request, product_id):
    return processViewProduct(request, product_id)


@extend_schema(
    request=ProductCreateUpdateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productCreate(request):
    return processCreateProduct(request)


@extend_schema(
    request=ProductCreateUpdateRequest,
    responses={200: schemaWrapper()},
    deprecated=True,
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productUpdate(request, product_id):
    return processUpdateProduct(request, product_id)


@extend_schema(
    request=ProductUpdateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productUpdateNutritionalInformation(request, product_id):
    return processUpdateProductNutritionalInformation(request, product_id)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def productDelete(request, product_id):
    return processDeleteProduct(request, product_id)


@extend_schema(
    request=ProductNutritionalInformationNERRequest,
    responses={200: schemaWrapper(ProductNutritionalInformationNERResponse)},
)
@parser_classes([MultiPartParser])
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=ProductNutritionalInformationNERResponse(allow_null=True))
def productNER(request):
    return processProductNutritionalInformationNER(request)


# endregion


# region Families
@extend_schema(
    parameters=[FamilySearchRequest],
    responses={200: schemaWrapper(FamilySearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=FamilySearchResponse(allow_null=True))
def familySearch(request):
    return processSearchFamilies(request)


@extend_schema(
    responses={200: schemaWrapper(FamilyDetailResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=FamilyDetailResponse(allow_null=True))
def familyDetails(request, family_id):
    return processViewFamily(request, family_id)


@extend_schema(
    request=FamilyCreateUpdateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def familyCreate(request):
    return processCreateFamily(request)


@extend_schema(
    request=FamilyCreateUpdateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def familyUpdate(request, family_id):
    return processUpdateFamily(request, family_id)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def familyDelete(request, family_id):
    return processDeleteFamily(request, family_id)


@extend_schema(
    responses={200: schemaWrapper(GenderDropdownResponse(many=True))},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=GenderDropdownResponse(allow_null=True, many=True))
def genderDropdown(request):
    return processRetrieveGenderDropdown(request)


@extend_schema(
    responses={200: schemaWrapper(ActivityLevelDropdownResponse(many=True))},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=ActivityLevelDropdownResponse(allow_null=True, many=True))
def activityLevelDropdown(request):
    return processRetrieveActivityLevelDropdown(request)


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
