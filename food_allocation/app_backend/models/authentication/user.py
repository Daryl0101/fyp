import uuid
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
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
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
