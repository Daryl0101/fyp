from rest_framework import serializers
from app_backend.models.authentication.user import User
from app_backend.serializers.base.response.paginationResponse import PaginationResponse


class UserSearchItemResponse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_ngo_manager",
        ]


class UserSearchResponse(PaginationResponse, serializers.Serializer):
    items = UserSearchItemResponse(many=True)
