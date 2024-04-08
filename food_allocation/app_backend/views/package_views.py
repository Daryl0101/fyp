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
from app_backend.serializers.package.request.packageSearchRequest import (
    PackageSearchRequest,
)
from app_backend.serializers.package.response.packageDetailResponse import (
    PackageDetailResponse,
)
from app_backend.serializers.package.response.packageSearchResponse import (
    PackageSearchResponse,
)
from app_backend.services.package_services import (
    processCancelPackage,
    processDeliverPackage,
    processPackPackage,
    processSearchPackages,
    processViewPackage,
)
from app_backend.utils import schemaWrapper


@extend_schema(
    parameters=[PackageSearchRequest],
    responses={200: schemaWrapper(PackageSearchResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=PackageSearchResponse(allow_null=True))
def packageSearch(request):
    return processSearchPackages(request)


@extend_schema(
    responses={200: schemaWrapper(PackageDetailResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=PackageDetailResponse(allow_null=True))
def packageDetails(request, package_id):
    return processViewPackage(request, package_id)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def packagePack(request, package_id):
    return processPackPackage(request, package_id)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def packageDeliver(request, package_id):
    return processDeliverPackage(request, package_id)


@extend_schema(
    request=[{"cancel_reason": serializers.CharField()}],
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def packageCancel(request, package_id):
    return processCancelPackage(request, package_id)
