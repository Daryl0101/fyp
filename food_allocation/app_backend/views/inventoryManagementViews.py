from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app_backend.serializers.inventory_management.request.inventorySearchRequest import (
    InventorySearchRequest,
)
from app_backend.serializers.inventory_management.response.inventorySearchResponse import (
    InventorySearchResponse,
)
from app_backend.services.inventoryManagementServices import processSearchInventory
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
    return processSearchInventory(request)


def inventoryView(request):
    pass


def inventoryCreate(request):
    pass


def inventoryUpdate(request):
    pass


def inventoryDelete(request):
    pass
