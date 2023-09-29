from rest_framework import serializers

from app_backend.enums import HalalStatus
from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class ProductSearchRequest(PaginationRequest, serializers.Serializer):
    product_no = serializers.CharField(
        max_length=100, allow_blank=True, required=False, default=""
    )
    product_name_or_description = serializers.CharField(
        max_length=100, allow_blank=True, required=False, default=""
    )
    halal_status = serializers.ChoiceField(
        choices=HalalStatus.choices, default=HalalStatus.ALL
    )
