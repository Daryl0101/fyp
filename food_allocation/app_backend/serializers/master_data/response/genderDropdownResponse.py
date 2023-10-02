from rest_framework import serializers


class GenderDropdownResponse(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
