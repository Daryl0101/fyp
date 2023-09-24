from rest_framework import serializers


class AuthenticationLoginRequest(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
