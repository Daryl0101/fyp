# Reference https://stackoverflow.com/a/64336918
# DateField and DateTimeField does not support allow_blank, only allow_null
from rest_framework import serializers
from rest_framework.fields import settings
from app_backend.enums import HalalStatus

from app_backend.serializers.base.request.paginationRequest import PaginationRequest


class InventorySearchRequest(PaginationRequest, serializers.Serializer):
    inventory_no = serializers.CharField(max_length=100, required=False, default="")
    product_no = serializers.CharField(max_length=100, required=False, default="")
    product_name = serializers.CharField(max_length=100, required=False, default="")
    storage_no = serializers.CharField(max_length=100, required=False, default="")
    storage_description = serializers.CharField(
        max_length=100, required=False, default=""
    )
    expiration_date_start = serializers.DateField(
        required=False,
        allow_null=True,
        default=None,
        input_formats=settings.DATE_INPUT_FORMATS,
    )
    expiration_date_end = serializers.DateField(
        required=False,
        allow_null=True,
        default=None,
        input_formats=settings.DATE_INPUT_FORMATS,
    )
    received_date_start = serializers.DateField(
        required=False,
        allow_null=True,
        default=None,
        input_formats=settings.DATE_INPUT_FORMATS,
    )
    received_date_end = serializers.DateField(
        required=False,
        allow_null=True,
        default=None,
        input_formats=settings.DATE_INPUT_FORMATS,
    )
    halal_status = serializers.ChoiceField(
        choices=HalalStatus.choices, default=HalalStatus.ALL
    )

    def validate(self, data):
        if bool(data["expiration_date_start"]) ^ bool(data["expiration_date_end"]):
            raise serializers.ValidationError(
                "Both Expiration Start and Expiration End dates must be provided"
            )
        elif (
            bool(data["expiration_date_start"]) & bool(data["expiration_date_end"])
            and data["expiration_date_start"] > data["expiration_date_end"]
        ):
            raise serializers.ValidationError(
                "Expiration Start date must be before Expiration End date"
            )

        if bool(data["received_date_start"]) ^ bool(data["received_date_end"]):
            raise serializers.ValidationError(
                "Both Received Start and Received End dates must be provided"
            )
        elif (
            bool(data["received_date_start"]) & bool(data["received_date_end"])
            and data["received_date_start"] > data["received_date_end"]
        ):
            raise serializers.ValidationError(
                "Received Start date must be before Received End date"
            )
        return data
