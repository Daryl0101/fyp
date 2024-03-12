from rest_framework import serializers

from app_backend.enums import HalalStatus
from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class StorageSearchRequest(PaginationRequest, serializers.Serializer):
    storage_no = serializers.CharField(
        max_length=100, allow_blank=True, required=False, default=""
    )
    description = serializers.CharField(
        max_length=100, allow_blank=True, required=False, default=""
    )
    halal_status = serializers.ChoiceField(
        choices=HalalStatus.choices, default=HalalStatus.ALL
    )
    exclude_product_id = serializers.IntegerField(
        allow_null=True, required=False, default=None
    )
