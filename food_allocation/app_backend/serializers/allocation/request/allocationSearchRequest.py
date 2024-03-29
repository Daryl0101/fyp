from rest_framework import serializers

from app_backend.enums import AllocationStatus
from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class AllocationSearchRequest(PaginationRequest, serializers.Serializer):
    allocation_no = serializers.CharField(required=False, allow_blank=True, default="")
    inventory_no = serializers.CharField(required=False, allow_blank=True, default="")
    # product_no = serializers.CharField(required=False, allow_blank=True, default="")
    family_no = serializers.CharField(required=False, allow_blank=True, default="")
    # created_on = serializers.DateField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=AllocationStatus.choices, required=False, allow_blank=True, default=""
    )
