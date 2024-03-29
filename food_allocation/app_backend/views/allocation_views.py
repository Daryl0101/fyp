from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from app_backend.decorators import response_handler
from app_backend.permissions import IsNGOManager
from app_backend.serializers.allocation.request.allocationCreateRequest import (
    AllocationCreateRequest,
)
from app_backend.serializers.allocation.request.allocationFamilySearchRequest import (
    AllocationFamilySearchRequest,
)
from app_backend.serializers.allocation.request.allocationInventorySearchRequest import (
    AllocationInventorySearchRequest,
)
from app_backend.serializers.allocation.request.allocationSearchRequest import (
    AllocationSearchRequest,
)
from app_backend.serializers.allocation.response.allocationDetailResponse import (
    AllocationDetailResponse,
)
from app_backend.serializers.allocation.response.allocationFamilySearchResponse import (
    AllocationFamilySearchResponse,
)
from app_backend.serializers.allocation.response.allocationInventorySearchResponse import (
    AllocationInventorySearchResponse,
)
from app_backend.serializers.allocation.response.allocationIsAllowedValidationResponse import (
    AllocationIsAllowedValidationResponse,
)
from app_backend.serializers.allocation.response.allocationSearchResponse import (
    AllocationSearchResponse,
)
from app_backend.services.allocation_services import (
    processRejectAllocationFamily,
    processSearchAllocationFamilies,
    processSearchAllocationInventories,
    processSearchAllocations,
    processValidateNewAllocationIsAllowed,
    processViewAllocation,
)
from app_backend.services_orchestration.allocation_services_orchestration import (
    processAcceptAllocationFamily,
    processCreateAllocation,
)
from app_backend.utils import schemaWrapper


@extend_schema(
    parameters=[AllocationSearchRequest],
    responses={200: schemaWrapper(AllocationSearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=AllocationSearchResponse(allow_null=True))
def allocationSearch(request):
    return processSearchAllocations(request)


@extend_schema(
    responses={200: schemaWrapper(AllocationDetailResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=AllocationDetailResponse(allow_null=True))
def allocationDetails(request, allocation_id):
    return processViewAllocation(request, allocation_id)


@extend_schema(
    parameters=[AllocationFamilySearchRequest],
    responses={200: schemaWrapper(AllocationFamilySearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=AllocationFamilySearchResponse(allow_null=True))
def allocationFamilySearch(request):
    return processSearchAllocationFamilies(request)


@extend_schema(
    parameters=[AllocationInventorySearchRequest],
    responses={200: schemaWrapper(AllocationInventorySearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=AllocationInventorySearchResponse(allow_null=True))
def allocationInventorySearch(request):
    return processSearchAllocationInventories(request)


@extend_schema(
    responses={200: schemaWrapper(AllocationIsAllowedValidationResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=AllocationIsAllowedValidationResponse(allow_null=True))
def allocationValidateCreateIsAllowed(request):
    return processValidateNewAllocationIsAllowed(request)


@extend_schema(
    request=AllocationCreateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def allocationCreate(request):
    return processCreateAllocation(request)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def allocationFamilyAccept(request, allocation_family_id):
    return processAcceptAllocationFamily(request, allocation_family_id)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def allocationFamilyReject(request, allocation_family_id):
    return processRejectAllocationFamily(request, allocation_family_id)
