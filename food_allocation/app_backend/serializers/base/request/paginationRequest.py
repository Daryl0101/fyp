from rest_framework import serializers


class PaginationRequest(serializers.Serializer):
    page_no = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=10)
    sort_column = serializers.CharField(default="Default")
