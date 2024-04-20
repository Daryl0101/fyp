from datetime import date, datetime, time
import os
from typing import List, TypedDict
from uuid import UUID
import firebase_admin
from firebase_admin import firestore
from rest_framework.serializers import ValidationError

from app_backend.enums import NotificationReadStatus
from app_backend.utils import isBlank

app = firebase_admin.initialize_app()
db = firestore.client()
notification_collection_ref = db.collection("notifications")
user_collection_ref = db.collection("users")


class Notification(TypedDict):
    user_id: str | UUID  # User Id of the user to send the notification to
    title: str  # The message title of the notification
    body: str  # The message body of the notification
    link: (
        str | None
    )  # The link to redirect the user to when the notification is clicked
    expiry: datetime  # The expiry time of the notification
    status: NotificationReadStatus


def addNotification(content: Notification):
    notification_collection_ref.add(
        {
            "user_id": str(content["user_id"]),
            "title": str(content["title"]),
            "body": str(content["body"]),
            "link": content["link"],
            "expiry": content["expiry"],
            "status": content["status"],
        }
    )


def addNotificationBatch(items: List[Notification]):
    batch = db.batch()
    for item in items:
        batch.set(
            notification_collection_ref.document(),
            {
                "user_id": str(item["user_id"]),
                "title": str(item["title"]),
                "body": str(item["body"]),
                "link": item["link"],
                "expiry": item["expiry"],
                "status": item["status"],
            },
        )
    batch.commit()


def processUpdateNotificationReadStatusToIsRead(request):
    result = False
    notification_id = request.data.get("notification_id")
    if isBlank(notification_id):
        raise ValidationError("Notification ID is required")
    doc = notification_collection_ref.document(notification_id)
    if not doc.get().exists:
        raise ValidationError("Notification not found")
    if doc.get().to_dict()["user_id"] != str(request.user.id):
        raise ValidationError("Cannot update notification not meant for you")
    if doc.get().to_dict()["status"] == NotificationReadStatus.READ:
        raise ValidationError("Cannot update read notification")
    doc.update({"status": NotificationReadStatus.READ})
    result = True
    return result


def processRemoveNotification(request, notification_id: str):
    result = False
    if isBlank(notification_id):
        raise ValidationError("Notification ID is required")
    doc = notification_collection_ref.document(notification_id)
    if not doc.get().exists:
        raise ValidationError("Notification not found")
    if doc.get().to_dict()["user_id"] != str(request.user.id):
        raise ValidationError("Cannot delete notification not meant for you")
    if doc.get().to_dict()["status"] == NotificationReadStatus.UNREAD:
        raise ValidationError("Cannot delete unread notification")
    doc.delete()
    result = True
    return result


def removeExpiredNotificationBatch():
    expired_notifications = notification_collection_ref.where(
        filter=firestore.firestore.FieldFilter(
            "expiry", "<=", datetime.combine(date.today(), time.min)
        )
    )
    if expired_notifications.count().get()[0][0].value <= 0:
        return
    batch = db.batch()
    expired_notifications = expired_notifications.stream()
    for noti in expired_notifications:
        batch.delete(noti.reference)
    batch.commit()


# region Firebase Cloud Messaging (FCM)
# region Public Functions


def processRegisterUserFCMToken(request):
    result = False

    fcm_token = request.data.get("fcm_token")
    if isBlank(fcm_token):
        raise ValidationError("FCM Token cannot be blank")
    transaction = db.transaction()
    registerUserFCMToken(transaction, request.user.id, fcm_token)

    result = True
    return result


def processUnregisterUserFCMToken(request):
    result = False

    fcm_token = request.data.get("fcm_token")
    if isBlank(fcm_token):
        raise ValidationError("FCM Token cannot be blank")
    transaction = db.transaction()
    unregisterUserFCMToken(transaction, request.user.id, fcm_token)

    result = True
    return result


# endregion


# region Private Functions
@firestore.firestore.transactional
def registerUserFCMToken(
    transaction: firestore.firestore.Transaction, user_id, fcm_token
):
    user = user_collection_ref.document(str(user_id))
    if not user.get().exists:
        transaction.set(
            user,
            {
                "tokens": [fcm_token],
            },
        )
    elif fcm_token not in user.get().get("tokens"):
        transaction.update(
            user, {"tokens": firestore.firestore.ArrayUnion([fcm_token])}
        )


@firestore.firestore.transactional
def unregisterUserFCMToken(
    transaction: firestore.firestore.Transaction, user_id, fcm_token
):
    user = user_collection_ref.document(str(user_id))
    user_snapshot = user.get()
    if user_snapshot.exists and fcm_token in user_snapshot.get("tokens"):
        if len(user_snapshot.get("tokens")) <= 1:
            transaction.delete(user)
        else:
            transaction.update(
                user, {"tokens": firestore.firestore.ArrayRemove([fcm_token])}
            )


# endregion


# endregion
