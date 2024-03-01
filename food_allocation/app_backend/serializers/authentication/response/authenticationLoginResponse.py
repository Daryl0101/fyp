from rest_framework import serializers


class AuthenticationLoginResponse(serializers.Serializer):
    id = serializers.UUIDField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_null=True)
    token = serializers.CharField(allow_null=True)
    role = serializers.CharField(allow_null=True)
