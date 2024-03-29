from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app_backend.serializers.inventory_management.request.inventoryAdjustRequest import (
    InventoryAdjustRequest,
)
from app_backend.serializers.inventory_management.request.inventoryInboundRequest import (
    InventoryInboundRequest,
)
from app_backend.serializers.inventory_management.request.inventorySearchRequest import (
    InventorySearchRequest,
)
from app_backend.serializers.inventory_management.response.inventoryDetailResponse import (
    InventoryDetailResponse,
)
from app_backend.serializers.inventory_management.response.inventorySearchResponse import (
    InventorySearchResponse,
)
from app_backend.services.inventory_management_services import (
    processAdjustInventory,
    processDeleteInventory,
    processSearchInventories,
    processViewInventory,
)
from app_backend.services_aggregation.inventory_management_services_aggregation import (
    processInboundInventory,
)
from app_backend.utils import schemaWrapper
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from app_backend.decorators import response_handler


@extend_schema(
    parameters=[InventorySearchRequest],
    responses={200: schemaWrapper(InventorySearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=InventorySearchResponse(allow_null=True))
def inventorySearch(request):
    return processSearchInventories(request)


@extend_schema(
    responses={200: schemaWrapper(InventoryDetailResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=InventoryDetailResponse(allow_null=True))
def inventoryDetails(request, inventory_id):
    return processViewInventory(request, inventory_id)


@extend_schema(
    request=InventoryInboundRequest,
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def inventoryInbound(request):
    return processInboundInventory(request)


@extend_schema(
    request=InventoryAdjustRequest,
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def inventoryAdjust(request, inventory_id):
    return processAdjustInventory(request, inventory_id)


@extend_schema(
    parameters=[InventoryAdjustRequest],  # pass 0 to the "qty" field from FE
    responses={200: schemaWrapper()},
)
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def inventoryDelete(request, inventory_id):
    return processDeleteInventory(request, inventory_id)
