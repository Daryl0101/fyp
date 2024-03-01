import uuid
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from app_backend.enums import Gender

from app_backend.models.base.common_model import BaseModel


class User(AbstractUser, BaseModel):
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
        auto_created=True,
    )
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20, default="", blank=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    profile_img_url = models.URLField(
        default=None, null=True, validators=[validators.URLValidator()]
    )
    gender = models.CharField(choices=Gender.choices)
    is_ngo_manager = models.BooleanField(default=False)
