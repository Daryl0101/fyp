import uuid
from django.db import models


class CommonModel:
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "User", on_delete=models.DO_NOTHING, default=uuid.UUID(int=0)
    )
    modified_by = models.ForeignKey(
        "User", on_delete=models.DO_NOTHING, default=uuid.UUID(int=0)
    )
