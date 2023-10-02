from rest_framework import serializers

from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class FoodCategorySearchRequest(PaginationRequest, serializers.Serializer):
    search_string = serializers.CharField(
        max_length=100, allow_blank=True, required=False, default=""
    )
