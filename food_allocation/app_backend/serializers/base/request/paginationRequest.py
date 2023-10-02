from rest_framework import serializers

from app_backend.enums import SortOrder


class PaginationRequest(serializers.Serializer):
    page_no = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=10)
    sort_column = serializers.CharField(default="default")
    sort_order = serializers.ChoiceField(
        choices=SortOrder.choices, default=SortOrder.ASCENDING
    )
