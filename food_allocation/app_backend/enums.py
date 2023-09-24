from django.db import models
from django.utils.translation import gettext_lazy as _


class ActionType(models.TextChoices):
    CREATE = "CREATE", _("Create")
    UPDATE = "UPDATE", _("Update")
