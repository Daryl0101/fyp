from rest_framework import serializers
from app_backend.enums import PackageStatus
from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class PackageSearchRequest(PaginationRequest, serializers.Serializer):
    package_no = serializers.CharField(required=False, allow_blank=True, default="")
    family_no = serializers.CharField(required=False, allow_blank=True, default="")
    allocation_no = serializers.CharField(required=False, allow_blank=True, default="")
    inventory_no = serializers.CharField(required=False, allow_blank=True, default="")
    product_no = serializers.CharField(required=False, allow_blank=True, default="")
    product_name = serializers.CharField(required=False, allow_blank=True, default="")
    status = serializers.ChoiceField(
        choices=PackageStatus.choices, required=False, allow_blank=True, default=""
    )
