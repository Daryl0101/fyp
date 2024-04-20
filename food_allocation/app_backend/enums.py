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


class ItemNoPrefix(models.TextChoices):
    FAMILY = "F", _("Family")
    INVENTORY = "INV", _("Inventory")
    PRODUCT = "P", _("Product")
    STORAGE = "S", _("Storage")
    ALLOCATION = "A", _("Allocation")
    PACKAGE = "PKG", _("Package")


class InventoryMovement(models.TextChoices):
    INBOUND = "INBOUND", _("Inbound")
    OUTBOUND = "OUTBOUND", _("Outbound")
    ADJUSTMENT = "ADJUSTMENT", _("Adjustment")
    # EXPIRED = "EXPIRED", _("Expired")
    # OTHER = "OTHER", _("Other")


class AllocationStatus(models.TextChoices):
    CREATED = "CREATED", _("Created")
    ONGOING = "ONGOING", _("Ongoing")
    SUCCESS = "SUCCESS", _("Success")
    FAILED = "FAILED", _("Failed")
    COMPLETED = "COMPLETED", _("Completed")


class AllocationFamilyStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    NOT_SERVED = "NOT_SERVED", _("Not Served")
    SERVED = "SERVED", _("Served")
    ACCEPTED = "ACCEPTED", _("Accepted")
    REJECTED = "REJECTED", _("Rejected")


class PackageStatus(models.TextChoices):
    NEW = "NEW", _("New")
    CANCELLED = "CANCELLED", _("Cancelled")
    PACKED = "PACKED", _("Packed")
    DELIVERED = "DELIVERED", _("Delivered")


class NotificationReadStatus(models.TextChoices):
    UNREAD = "UNREAD", _("Unread")
    READ = "READ", _("Read")


class Interval(models.TextChoices):
    # SECOND = "SECOND", _("Second")
    # MINUTE = "MINUTE", _("Minute")
    # HOUR = "HOUR", _("Hour")
    DAY = "DAY", _("Day")
    WEEK = "WEEK", _("Week")
    MONTH = "MONTH", _("Month")
    YEAR = "YEAR", _("Year")
