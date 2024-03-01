from rest_framework import serializers

from app_backend.serializers.base.request.paginationRequest import PaginationRequest
from app_backend.enums import Gender


class UserSearchRequest(PaginationRequest, serializers.Serializer):
    wildcard = serializers.CharField(
        max_length=150, allow_blank=True, required=False, default=""
    )
    is_ngo_manager = serializers.BooleanField(
        required=False, allow_null=True, default=None
    )
    gender = serializers.ChoiceField(
        choices=Gender.choices, required=False, allow_null=True, default=None
    )
