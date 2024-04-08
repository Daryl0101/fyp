from app_backend.enums import PackageStatus
from app_backend.models.base.common_model import BaseModel
from django.db import models


class PackageHistory(BaseModel):
    package = models.ForeignKey(
        "Package", on_delete=models.PROTECT, related_name="package_histories"
    )
    action = models.CharField(max_length=50, choices=PackageStatus.choices)
    cancel_reason = models.CharField(max_length=255, blank=True, default="")
