from rest_framework import serializers
from app_backend.enums import HalalStatus

from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class InventorySearchRequest(PaginationRequest, serializers.Serializer):
    product_no = serializers.CharField(max_length=100, required=False, default="")
    product_name = serializers.CharField(max_length=100, required=False, default="")
    storage_name = serializers.CharField(max_length=100, required=False, default="")
    expiration_date_start = serializers.DateField(required=False)
    expiration_date_end = serializers.DateField(required=False)
    batch_no = serializers.CharField(max_length=100, required=False, default="")
    received_date_start = serializers.DateField(required=False)
    received_date_end = serializers.DateField(required=False)
    halal_status = serializers.ChoiceField(
        choices=HalalStatus.choices, default=HalalStatus.ALL
    )
