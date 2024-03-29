import uuid
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from app_backend.enums import Gender


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
        default=None,
        null=True,
        # , validators=[validators.URLValidator()]
    )
    gender = models.CharField(choices=Gender.choices)
    is_ngo_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # created_by and modified_by can be referenced to User model using foreign key because is_active is used in the User model
    # these fields should not be blank or null
    # blank or null is here because of the initial migration
    # createsuperuser command will not work without these fields being blank or null
    created_by = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username
