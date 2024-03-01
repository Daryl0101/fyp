from django.db import models
from django.utils.translation import gettext_lazy as _


class SortOrder(models.IntegerChoices):
    ASCENDING = 0, _("Ascending")
    DESCENDING = 1, _("Descending")


class ActionType(models.TextChoices):
    CREATE = "CREATE", _("Create")
    UPDATE = "UPDATE", _("Update")


class Gender(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")


class ActivityLevel(models.IntegerChoices):
    SEDENTARY = 1, _("Sedentary")
    LIGHTLY_ACTIVE = 2, _("Lightly Active")
    MODERATELY_ACTIVE = 3, _("Moderately Active")
    VERY_ACTIVE = 4, _("Very Active")
    EXTRA_ACTIVE = 5, _("Extra Active")


class HalalStatus(models.IntegerChoices):
    ALL = 0, _("All")
    HALAL = 1, _("Halal")
    NON_HALAL = 2, _("Non Halal")


class Role(models.TextChoices):
    MANAGER = "MANAGER", _("manager")
    VOLUNTEER = "VOLUNTEER", _("volunteer")
