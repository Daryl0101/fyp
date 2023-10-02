from rest_framework import serializers


class AuthenticationRegisterLoginResponse(serializers.Serializer):
    username = serializers.CharField(allow_null=True)
    email = serializers.EmailField(allow_null=True)
    token = serializers.CharField(allow_null=True)
