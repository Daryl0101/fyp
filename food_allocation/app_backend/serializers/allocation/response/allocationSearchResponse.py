from rest_framework import serializers

from app_backend.models.allocation.allocation import Allocation
from app_backend.serializers.base.response.paginationResponse import PaginationResponse


class AllocationSearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = [
            "id",
            "allocation_no",
            "start_time",
            "end_time",
            "status",
        ]


class AllocationSearchResponse(PaginationResponse, serializers.Serializer):
    items = AllocationSearchItemResponse(many=True)
