from rest_framework import serializers

from app_backend.enums import Interval


class PeriodIntervalRequest(serializers.Serializer):
    interval = serializers.ChoiceField(choices=Interval.choices, default=Interval.DAY)
