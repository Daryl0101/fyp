from rest_framework import serializers
from app_backend.serializers.base.response.paginationResponse import PaginationResponse
from app_backend.models.master_data.family import Family


class FamilySearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["id", "family_no", "name", "last_received_date", "is_halal"]


class FamilySearchResponse(PaginationResponse, serializers.Serializer):
    families = FamilySearchItemResponse(many=True)
