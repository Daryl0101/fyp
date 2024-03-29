import datetime
from rest_framework import serializers
from rest_framework.compat import settings
from app_backend.enums import ActivityLevel, Gender


class PersonCreateUpdateRequest(serializers.Serializer):
    id = serializers.IntegerField(default=0)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    gender = serializers.ChoiceField(choices=Gender.choices)
    birthdate = serializers.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    height = serializers.DecimalField(max_digits=10, decimal_places=2)
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    activity_level = serializers.ChoiceField(choices=ActivityLevel.choices)

    def validate(self, data):
        if data["height"] <= 0:
            raise serializers.ValidationError("Invalid height")
        if data["weight"] <= 0:
            raise serializers.ValidationError("Invalid weight")
        if data["birthdate"] > datetime.date.today():
            raise serializers.ValidationError("Invalid birthdate")
        return data


class FamilyCreateUpdateRequest(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_halal = serializers.BooleanField()
    household_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=200, allow_blank=True)
    calorie_discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    food_restrictions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    members = PersonCreateUpdateRequest(many=True)

    def validate(self, data):
        if data["calorie_discount"] < 0 or data["calorie_discount"] >= 100:
            raise serializers.ValidationError("Invalid calorie discount")
        if data["household_income"] < 0:
            raise serializers.ValidationError("Invalid household income")
        if data["food_restrictions"] is not None:
            if list(filter(lambda x: x <= 0, data["food_restrictions"])):
                raise serializers.ValidationError("Invalid food category id(s)")
            if len(set(data["food_restrictions"])) != len(data["food_restrictions"]):
                raise serializers.ValidationError(
                    "Duplicate food category ids detected"
                )
        if data["members"] is None or len(data["members"]) <= 0:
            raise serializers.ValidationError("At least 1 member is required")
        if len(
            set(
                x["first_name"].lower() + x["last_name"].lower()
                for x in data["members"]
            )
        ) != len(data["members"]):
            raise serializers.ValidationError("Duplicate members detected")
        non_zero_member_ids = [
            x["id"] for x in data["members"] if x["id"] > 0 and x["id"] is not None
        ]
        if len(set(non_zero_member_ids)) != len(non_zero_member_ids):
            raise serializers.ValidationError("Duplicate member ids detected")
        return data

    def existing_members(self):
        return [
            x
            for x in self.validated_data["members"]
            if x["id"] > 0 and x["id"] is not None
        ]

    def new_members(self):
        return [
            x for x in self.validated_data["members"] if x["id"] <= 0 or x["id"] is None
        ]
