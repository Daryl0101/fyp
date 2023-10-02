from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from app_backend.models.authentication.user import User
from app_backend.serializers.authentication.request.authenticationLoginRequest import (
    AuthenticationLoginRequest,
)
from app_backend.serializers.authentication.request.authenticationRegisterRequest import (
    AuthenticationRegisterRequest,
)
from app_backend.serializers.authentication.response.authenticationRegisterLoginResponse import (
    AuthenticationRegisterLoginResponse,
)
from app_backend.serializers.authentication.response.authenticationProfileResponse import (
    AuthenticationProfileResponse,
)


@transaction.atomic
def processRegisterUser(request):
    # Check if request is valid
    request_parsed = AuthenticationRegisterRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # Create user
    user = User.objects.create_user(
        username=request_parsed.validated_data["username"],
        password=request_parsed.validated_data["password"],
        email=request_parsed.validated_data["email"],
        phone_number=request_parsed.validated_data["phone_number"],
        first_name=request_parsed.validated_data["first_name"].capitalize(),
        last_name=request_parsed.validated_data["last_name"].capitalize(),
    )
    if user is None:
        raise serializers.ValidationError("User creation failed")

    access_token = Token.objects.create(user=user)
    if access_token is None:
        raise serializers.ValidationError("Token creation failed")

    response_serializer = AuthenticationRegisterLoginResponse(
        data={
            "username": user.username,
            "email": user.email,
            "token": access_token.key,
        }
    )

    return response_serializer.initial_data


def processLoginUser(request):
    # Check if request is valid
    request_parsed = AuthenticationLoginRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # Authenticate user
    user = authenticate(
        username=request_parsed.validated_data["username"],
        password=request_parsed.validated_data["password"],
    )
    if user is None:
        raise serializers.ValidationError("User does not exist")

    # Get or create user's token
    access_token, is_created = Token.objects.get_or_create(user=user)
    if access_token is None:
        raise serializers.ValidationError("Token creation failed")

    # Login user
    login(request, user)

    response_serializer = AuthenticationRegisterLoginResponse(
        data={
            "username": user.username,
            "email": user.email,
            "token": access_token.key,
        }
    )

    return response_serializer.initial_data


def processLogoutUser(request):
    result = False

    logout(request)
    request.auth.delete()

    result = True
    return result


def processDisplayUserProfile(request):
    if request.user is None:
        raise serializers.ValidationError("User does not exist")

    response_serializer = AuthenticationProfileResponse(
        data={
            "username": request.user.username,
            "email": request.user.email,
            "phone_number": request.user.phone_number,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "date_joined": request.user.date_joined,
        }
    )

    return response_serializer.initial_data
