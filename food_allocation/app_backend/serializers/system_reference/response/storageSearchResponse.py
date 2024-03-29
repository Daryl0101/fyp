from rest_framework import serializers

from app_backend.models.system_reference.storage import Storage
from app_backend.serializers.base.response.paginationResponse import PaginationResponse


class StorageSearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id", "storage_no", "description", "is_halal"]


class StorageSearchResponse(PaginationResponse, serializers.Serializer):
    items = StorageSearchItemResponse(many=True)
