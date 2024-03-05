from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from app_backend.decorators import response_handler
from app_backend.serializers.system_reference.request.foodCategorySearchRequest import (
    FoodCategorySearchRequest,
)
from app_backend.serializers.system_reference.request.storageSearchRequest import (
    StorageSearchRequest,
)
from app_backend.serializers.system_reference.response.foodCategorySearchResponse import (
    FoodCategorySearchResponse,
)
from app_backend.serializers.system_reference.response.storageSearchResponse import (
    StorageSearchResponse,
)
from app_backend.services.systemReferenceServices import (
    processSearchFoodCategories,
    processSearchStorages,
)
from app_backend.utils import schemaWrapper


@extend_schema(
    parameters=[FoodCategorySearchRequest],
    responses={200: schemaWrapper(FoodCategorySearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=FoodCategorySearchResponse(allow_null=True))
def foodCategoriesSearch(request):
    return processSearchFoodCategories(request)


@extend_schema(
    parameters=[StorageSearchRequest],
    responses={200: schemaWrapper(StorageSearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=StorageSearchResponse(allow_null=True))
def storagesSearch(request):
    return processSearchStorages(request)
