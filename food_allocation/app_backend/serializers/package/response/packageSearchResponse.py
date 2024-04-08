from rest_framework import serializers
from app_backend.models.package.package import Package
from app_backend.serializers.allocation.response.allocationSearchResponse import (
    AllocationSearchItemResponse,
)
from app_backend.serializers.base.response.paginationResponse import PaginationResponse
from app_backend.serializers.master_data.response.familySearchResponse import (
    FamilySearchItemResponse,
)


class PackageSearchItemResponse(serializers.ModelSerializer):
    family = FamilySearchItemResponse()
    allocation = AllocationSearchItemResponse()
    created_by = serializers.CharField()
    modified_by = serializers.CharField()

    class Meta:
        model = Package
        exclude = ["allocation_family"]


class PackageSearchResponse(PaginationResponse, serializers.Serializer):
    items = PackageSearchItemResponse(many=True)
