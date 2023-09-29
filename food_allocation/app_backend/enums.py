from django.db import models
from django.utils.translation import gettext_lazy as _


class ActionType(models.TextChoices):
    CREATE = "CREATE", _("Create")
    UPDATE = "UPDATE", _("Update")


class Gender(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")


class ActivityLevel(models.TextChoices):
    SEDENTARY = "SEDENTARY", _("Sedentary")
    LIGHTLY_ACTIVE = "LIGHTLY_ACTIVE", _("Lightly Active")
    MODERATELY_ACTIVE = "MODERATELY_ACTIVE", _("Moderately Active")
    VERY_ACTIVE = "VERY_ACTIVE", _("Very Active")
    EXTRA_ACTIVE = "EXTRA_ACTIVE", _("Extra Active")


class HalalStatus(models.IntegerChoices):
    ALL = 0, _("All")
    HALAL = 1, _("Halal")
    NON_HALAL = 2, _("Non Halal")
