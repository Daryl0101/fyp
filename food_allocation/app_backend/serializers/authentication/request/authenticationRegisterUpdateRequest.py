from rest_framework import serializers
from app_backend.enums import Gender


class AuthenticationRegisterUpdateRequest(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    email = serializers.EmailField(max_length=254)
    phone_number = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    is_ngo_manager = serializers.BooleanField(required=True)
    gender = serializers.ChoiceField(choices=Gender.choices, required=True)
