import uuid
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from app_backend.enums import ActionType, Gender, Role, SortOrder
from app_backend.models.authentication.user import User
from app_backend.serializers.authentication.request.authenticationLoginRequest import (
    AuthenticationLoginRequest,
)
from app_backend.serializers.authentication.request.authenticationRegisterUpdateRequest import (
    AuthenticationRegisterUpdateRequest,
)
from app_backend.serializers.authentication.request.userSearchRequest import (
    UserSearchRequest,
)
from app_backend.serializers.authentication.response.authenticationLoginResponse import (
    AuthenticationLoginResponse,
)
from app_backend.serializers.authentication.response.authenticationProfileResponse import (
    AuthenticationProfileResponse,
)
from app_backend.serializers.authentication.response.userSearchResponse import (
    UserSearchItemResponse,
    UserSearchResponse,
)
from app_backend.utils import isBlank, setCreateUpdateProperty


@transaction.atomic
def processRegisterUser(request):
    result = False
    # Check if request is valid
    request_parsed = AuthenticationRegisterUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # Create user
    user = User.objects.create_user(
        username=request_parsed.validated_data["username"],
        password=request_parsed.validated_data["password"],
        email=request_parsed.validated_data["email"],
        phone_number=request_parsed.validated_data["phone_number"],
        first_name=request_parsed.validated_data["first_name"].capitalize(),
        last_name=request_parsed.validated_data["last_name"].capitalize(),
        gender=request_parsed.validated_data["gender"],
        is_ngo_manager=request_parsed.validated_data["is_ngo_manager"],
        created_by=request.user.id,
        modified_by=request.user.id,
    )
    # setCreateUpdateProperty(user, request.user, ActionType.CREATE)
    user.save()

    if user is None:
        raise serializers.ValidationError("User creation failed")

    result = True
    return result


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

    response_serializer = AuthenticationLoginResponse(
        data={
            "id": user.id,
            "name": user.username,
            "email": user.email,
            "token": access_token.key,
            "role": Role.MANAGER.label if user.is_ngo_manager else Role.VOLUNTEER.label,
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
            "is_ngo_manager": request.user.is_ngo_manager,
            "date_joined": request.user.date_joined,
            "gender": request.user.gender,
        }
    )

    return response_serializer.initial_data


def processSearchUser(request):
    # region Parse request
    request_parsed = UserSearchRequest(data=request.query_params)
    request_parsed.is_valid(raise_exception=True)
    # endregion

    # region Filter
    users = User.objects.all().filter(is_active=True)

    if not isBlank(request_parsed.validated_data["wildcard"]):
        users = users.filter(
            Q(username__icontains=request_parsed.validated_data["wildcard"])
            | Q(email__icontains=request_parsed.validated_data["wildcard"])
            | Q(first_name__icontains=request_parsed.validated_data["wildcard"])
            | Q(last_name__icontains=request_parsed.validated_data["wildcard"])
        )

    if request_parsed.validated_data["is_ngo_manager"] is not None:
        users = users.filter(
            is_ngo_manager=request_parsed.validated_data["is_ngo_manager"]
        )

    if request_parsed.validated_data["gender"] == Gender.MALE:
        users = users.filter(gender=Gender.MALE)
    elif request_parsed.validated_data["gender"] == Gender.FEMALE:
        users = users.filter(gender=Gender.FEMALE)
    # endregion

    # region Sort
    fields = UserSearchItemResponse().fields
    scso = "modified_at"

    if request_parsed.validated_data["sort_column"] in fields.keys():
        scso = request_parsed.validated_data["sort_column"]
    if request_parsed.validated_data["sort_order"] == SortOrder.DESCENDING:
        scso = "-" + scso

    users = users.order_by(scso)

    # endregion

    # region Pagination
    paginator = Paginator(
        object_list=users, per_page=request_parsed.validated_data["page_size"]
    )
    page = paginator.get_page(request_parsed.validated_data["page_no"])
    # endregion

    # region Serialize response
    response_serializer = UserSearchResponse(
        data={
            "items": UserSearchItemResponse(
                page.object_list, many=True, allow_null=True
            ).data,
            "total_page": paginator.num_pages,
            "current_page": page.number,
            "next_page": page.next_page_number() if page.has_next() else None,
            "previous_page": (
                page.previous_page_number() if page.has_previous() else None
            ),
            "total_record": paginator.count,
            "current_record": page.object_list.count(),
        }
    )
    # endregion
    return response_serializer.initial_data


def processRetrieveUserDetails(request, user_id: uuid):
    user = User.objects.filter(is_active=True).filter(id=user_id).first()
    if user is None:
        raise serializers.ValidationError("User does not exist")

    response_serializer = AuthenticationProfileResponse(
        data={
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_ngo_manager": user.is_ngo_manager,
            "date_joined": user.date_joined,
            "gender": user.gender,
        }
    )

    return response_serializer.initial_data


def processUpdateUser(request, user_id: uuid):
    result = False
    # Check if request is valid
    request_parsed = AuthenticationRegisterUpdateRequest(data=request.data)
    request_parsed.is_valid(raise_exception=True)

    # Update user
    user = User.objects.filter(is_active=True).filter(id=user_id).first()
    if user is None:
        raise serializers.ValidationError("User does not exist")

    user.username = request_parsed.validated_data["username"]
    user.password = request_parsed.validated_data["password"]
    user.email = request_parsed.validated_data["email"]
    user.phone_number = request_parsed.validated_data["phone_number"]
    user.first_name = request_parsed.validated_data["first_name"].capitalize()
    user.last_name = request_parsed.validated_data["last_name"].capitalize()
    user.is_ngo_manager = request_parsed.validated_data["is_ngo_manager"]
    user.gender = request_parsed.validated_data["gender"]
    setCreateUpdateProperty(user, request.user, ActionType.UPDATE)

    user.save()

    result = True
    return result


def processDeleteUser(request, user_id: uuid):
    result = False
    user = User.objects.filter(is_active=True).filter(id=user_id).first()
    if user is None:
        raise serializers.ValidationError("User does not exist")

    user.is_active = False
    user.save()

    result = True
    return result
