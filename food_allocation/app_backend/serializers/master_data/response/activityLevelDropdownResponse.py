from rest_framework import serializers


class ActivityLevelDropdownResponse(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
