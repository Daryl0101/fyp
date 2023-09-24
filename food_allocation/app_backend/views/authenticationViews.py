from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema
from app_backend.serializers.authentication.response.authenticationProfileResponse import (
    AuthenticationProfileResponse,
)
from app_backend.utils import baseResponseSerializerGenerator
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from app_backend.serializers.authentication.request.authenticationLoginRequest import (
    AuthenticationLoginRequest,
)
from app_backend.serializers.authentication.response.authenticationLoginResponse import (
    AuthenticationLoginResponse,
)
from app_backend.decorators import response_handler
from app_backend.services.authenticationServices import *


class AuthenticationViews(viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AuthenticationRegisterRequest,
        responses={
            200: baseResponseSerializerGenerator(
                model=AuthenticationLoginResponse(allow_null=True)
            )
        },
    )
    @action(
        methods=["POST"],
        url_path="register",
        detail=False,
        permission_classes=[AllowAny],
    )
    @response_handler(responses=AuthenticationLoginResponse(allow_null=True))
    def authenticationRegister(self, request):
        return processRegisterUser(request)

    @extend_schema(
        request=AuthenticationLoginRequest,
        responses={
            200: baseResponseSerializerGenerator(
                model=AuthenticationLoginResponse(allow_null=True)
            )
        },
    )
    @action(
        methods=["POST"],
        url_path="login",
        detail=False,
        permission_classes=[AllowAny],
    )
    @response_handler(responses=AuthenticationLoginResponse(allow_null=True))
    def authenticationLogin(self, request):
        return processLoginUser(request)

    @extend_schema(
        responses={
            200: baseResponseSerializerGenerator(
                model=serializers.BooleanField(allow_null=True)
            )
        },
    )
    @action(
        methods=["POST"],
        url_path="logout",
        detail=False,
    )
    @response_handler(responses=serializers.BooleanField(allow_null=True))
    def authenticationLogout(self, request):
        return processLogoutUser(request)

    @extend_schema(
        responses={
            200: baseResponseSerializerGenerator(
                model=AuthenticationProfileResponse(allow_null=True)
            )
        },
    )
    @action(
        methods=["GET"],
        url_path="profile",
        detail=False,
    )
    @response_handler(responses=AuthenticationProfileResponse(allow_null=True))
    def authenticationDisplayProfile(self, request):
        return processDisplayUserProfile(request)
