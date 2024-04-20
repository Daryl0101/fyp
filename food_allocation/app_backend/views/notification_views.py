from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from app_backend.services.notification_services import (
    processRegisterUserFCMToken,
    processRemoveNotification,
    processUnregisterUserFCMToken,
    processUpdateNotificationReadStatusToIsRead,
)
from app_backend.utils import schemaWrapper
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from app_backend.permissions import IsNGOManager
from rest_framework.permissions import IsAuthenticated
from app_backend.decorators import response_handler


@extend_schema(
    request=[{"notification_id": serializers.CharField()}],
    responses={200: schemaWrapper()},
)
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def notificationMarkAsRead(request):
    return processUpdateNotificationReadStatusToIsRead(request)


@extend_schema(
    responses={200: schemaWrapper()},
)
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def notificationDelete(request, notification_id):
    return processRemoveNotification(request, notification_id)


@extend_schema(
    request=[{"fcm_token": serializers.CharField()}],
    responses={200: schemaWrapper()},
)
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def registerUserFCMToken(request):
    return processRegisterUserFCMToken(request)


@extend_schema(
    request=[{"fcm_token": serializers.CharField()}],
    responses={200: schemaWrapper()},
)
@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@response_handler(responses=serializers.BooleanField(allow_null=True))
def unregisterUserFCMToken(request):
    return processUnregisterUserFCMToken(request)
