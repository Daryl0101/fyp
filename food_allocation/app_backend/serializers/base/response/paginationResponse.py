from rest_framework import serializers


class PaginationResponse(serializers.Serializer):
    total_page = serializers.IntegerField(allow_null=True, default=None)
    current_page = serializers.IntegerField(allow_null=True, default=None)
    next_page = serializers.IntegerField(allow_null=True, default=None)
    previous_page = serializers.IntegerField(allow_null=True, default=None)
    total_record = serializers.IntegerField(allow_null=True, default=None)
    current_record = serializers.IntegerField(allow_null=True, default=None)
