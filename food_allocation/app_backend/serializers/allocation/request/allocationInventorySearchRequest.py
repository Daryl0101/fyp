from rest_framework import serializers

from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class AllocationInventorySearchRequest(PaginationRequest, serializers.Serializer):
    allocation_id = serializers.IntegerField()
