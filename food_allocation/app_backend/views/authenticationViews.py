from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema
from app_backend.permissions import IsNGOManager
from app_backend.serializers.authentication.request.authenticationRegisterUpdateRequest import (
    AuthenticationRegisterUpdateRequest,
)
from app_backend.serializers.authentication.request.userSearchRequest import (
    UserSearchRequest,
)
from app_backend.serializers.authentication.response.authenticationProfileResponse import (
    AuthenticationProfileResponse,
)
from app_backend.serializers.authentication.response.userSearchResponse import (
    UserSearchResponse,
)
from app_backend.services.authenticationServices import (
    processDeleteUser,
    processDisplayUserProfile,
    processLoginUser,
    processLogoutUser,
    processRegisterUser,
    processRetrieveUserDetails,
    processSearchUser,
    processUpdateUser,
)
from app_backend.utils import schemaWrapper
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from app_backend.serializers.authentication.request.authenticationLoginRequest import (
    AuthenticationLoginRequest,
)
from app_backend.serializers.authentication.response.authenticationLoginResponse import (
    AuthenticationLoginResponse,
)
from app_backend.decorators import response_handler


@extend_schema(
    request=AuthenticationRegisterUpdateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def authenticationRegister(request):
    return processRegisterUser(request)


@extend_schema(
    request=AuthenticationLoginRequest,
    responses={200: schemaWrapper(AuthenticationLoginResponse)},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
@response_handler(responses=AuthenticationLoginResponse(allow_null=True))
def authenticationLogin(request):
    return processLoginUser(request)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def authenticationLogout(request):
    return processLogoutUser(request)


@extend_schema(
    responses={200: schemaWrapper(AuthenticationProfileResponse)},
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=AuthenticationProfileResponse(allow_null=True))
def authenticationDisplayProfile(request):
    return processDisplayUserProfile(request)


@extend_schema(
    parameters=[UserSearchRequest], responses={200: schemaWrapper(UserSearchResponse)}
)
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=UserSearchResponse(allow_null=True))
def authenticationSearchUser(request):
    return processSearchUser(request)


@extend_schema(responses={200: schemaWrapper(AuthenticationProfileResponse)})
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=AuthenticationProfileResponse(allow_null=True))
def authenticationUserDetails(request, user_id):
    return processRetrieveUserDetails(request, user_id)


@extend_schema(
    request=AuthenticationRegisterUpdateRequest,
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def authenticationUpdateUser(request, user_id):
    return processUpdateUser(request, user_id)


@extend_schema(responses={200: schemaWrapper()})
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, IsNGOManager])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def authenticationDeleteUser(request, user_id):
    return processDeleteUser(request, user_id)


# class AuthenticationViews(viewsets.GenericViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     @extend_schema(
#         request=AuthenticationRegisterRequest,
#         responses={
#             200: baseResponseSerializerGenerator(
#                 model=AuthenticationLoginResponse(allow_null=True)
#             )
#         },
#     )
#     @action(
#         methods=["POST"],
#         url_path="register",
#         detail=False,
#         permission_classes=[AllowAny],
#     )
#     @response_handler(responses=AuthenticationLoginResponse(allow_null=True))
#     def authenticationRegister(self, request):
#         return processRegisterUser(request)

#     @extend_schema(
#         request=AuthenticationLoginRequest,
#         responses={
#             200: baseResponseSerializerGenerator(
#                 model=AuthenticationLoginResponse(allow_null=True)
#             )
#         },
#     )
#     @action(
#         methods=["POST"],
#         url_path="login",
#         detail=False,
#         permission_classes=[AllowAny],
#     )
#     @response_handler(responses=AuthenticationLoginResponse(allow_null=True))
#     def authenticationLogin(self, request):
#         return processLoginUser(request)

#     @extend_schema(
#         responses={
#             200: baseResponseSerializerGenerator(
#                 model=serializers.BooleanField(allow_null=True)
#             )
#         },
#     )
#     @action(
#         methods=["POST"],
#         url_path="logout",
#         detail=False,
#     )
#     @response_handler(responses=serializers.BooleanField(allow_null=True))
#     def authenticationLogout(self, request):
#         return processLogoutUser(request)

#     @extend_schema(
#         responses={
#             200: baseResponseSerializerGenerator(
#                 model=AuthenticationProfileResponse(allow_null=True)
#             )
#         },
#     )
#     @action(
#         methods=["GET"],
#         url_path="profile",
#         detail=False,
#     )
#     @response_handler(responses=AuthenticationProfileResponse(allow_null=True))
#     def authenticationDisplayProfile(self, request):
#         return processDisplayUserProfile(request)
