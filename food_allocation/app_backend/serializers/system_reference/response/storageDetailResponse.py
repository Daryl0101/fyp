from rest_framework import serializers
from app_backend.models.system_reference.storage import Storage


class StorageDetailResponse(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"
