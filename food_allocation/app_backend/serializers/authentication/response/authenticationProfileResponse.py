from rest_framework import serializers


class AuthenticationProfileResponse(serializers.Serializer):
    username = serializers.CharField(allow_null=True, allow_blank=True)
    email = serializers.EmailField(allow_null=True, allow_blank=True)
    phone_number = serializers.CharField(allow_null=True, allow_blank=True)
    first_name = serializers.CharField(allow_null=True, allow_blank=True)
    last_name = serializers.CharField(allow_null=True, allow_blank=True)
    date_joined = serializers.DateTimeField(allow_null=True)
