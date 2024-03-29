from rest_framework import serializers

from app_backend.serializers.allocation.response.allocationDetailResponse import (
    AllocationDetailResponse,
)


class AllocationIsAllowedValidationResponse(serializers.Serializer):
    is_allowed = serializers.BooleanField()
    current_allocation = AllocationDetailResponse(allow_null=True)
