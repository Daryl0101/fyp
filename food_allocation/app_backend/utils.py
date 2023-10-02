import datetime
import inspect
import operator
from typing import Optional, Type
from django.db import models
from rest_framework import serializers
from app_backend.constants import FAILED_DICT, SUCCESS_DICT
from app_backend.enums import ActionType

from app_backend.models.authentication.user import User


def setCreateUpdateProperty(model, userObject: User, actionType: ActionType):
    try:
        if model is None or userObject is None:
            raise serializers.ValidationError("Model or UserObject is None")
        model.modified_by = userObject.id
        if actionType == ActionType.CREATE:
            model.created_by = userObject.id
    except Exception as ex:
        raise ex


generatorCalledCount = 0


def baseResponseSerializerGenerator(
    model: Type[serializers.Serializer | dict],
    isInstance: bool = False,
    value: Optional[serializers.Serializer | serializers.Field | dict | None] = None,
    errors: Optional[serializers.ValidationError | None] = None,
):
    global generatorCalledCount
    generatorCalledCount = generatorCalledCount + 1

    def with_content(
        self,
        value: Optional[
            serializers.Serializer | serializers.Field | dict | None
        ] = None,
        errors: Optional[serializers.ValidationError | None] = None,
    ):
        if self.is_valid(raise_exception=True):
            if value is not None:
                self.validated_data["model"] = value
            if errors is not None:
                # Normalize errors into a list of strings.
                errors_messages = []
                if isinstance(errors.detail, serializers.ReturnDict) or isinstance(
                    errors.detail, dict
                ):
                    print(errors.detail)
                    for field_name, field_errors in errors.detail.items():
                        for field_error in field_errors:
                            error_message = f"{field_name}: {field_error}"
                            errors_messages.append(
                                error_message
                            )  # append error message to 'errors_messages'
                elif isinstance(errors.detail, serializers.ReturnList) or isinstance(
                    errors.detail, list
                ):
                    errors_messages = errors.detail
                else:
                    errors_messages = [errors.detail]
                self.validated_data["errors"] = errors_messages
                # [
                #     {
                #         "code": error.code,
                #         "detail": str(error),
                #     }
                #     for error in errors.detail
                # ]
            return self

    # class_name = f"BaseResponseSerializer_{generatorCalledCount}"
    class_name = model.__class__.__name__
    base_classes = (serializers.Serializer,)
    class_attrs = {
        "with_content": with_content,
        "status_name": serializers.CharField(max_length=100, default="Success"),
        # "errors": serializers.DictField(
        #     allow_null=True,
        #     default={"errorCode": ""},
        #     child=serializers.ListField(
        #         child=serializers.CharField(max_length=100),
        #         allow_null=True,
        #     ),
        # ),
        "errors": serializers.ListField(
            child=serializers.CharField(max_length=100),
            allow_null=True,
        ),
        "model": model,
    }

    if model is None:
        return type(class_name, base_classes, class_attrs)(
            data=FAILED_DICT
        ).with_content(errors=serializers.ValidationError("Model is required."))

    if isInstance and not operator.xor(value is None, errors is None):
        return type(class_name, base_classes, class_attrs)(
            data=FAILED_DICT
        ).with_content(
            errors=serializers.ValidationError(
                "If isInstance is true, either value or errors is required."
            )
        )

    if not isInstance:
        return type(class_name, base_classes, class_attrs)

    if value is not None:
        return type(class_name, base_classes, class_attrs)(
            data=SUCCESS_DICT
        ).with_content(value=value)
    if errors is not None:
        return type(class_name, base_classes, class_attrs)(
            data=FAILED_DICT
        ).with_content(errors=errors)

    else:
        return type(class_name, base_classes, class_attrs)(
            data=FAILED_DICT
        ).with_content(
            errors=serializers.ValidationError(
                f"""
                Unhandled Exception in BaseResponseSerializerGenerator.
                'model': {model}, 
                'isInstance': {isInstance}, 
                'value': {value}, 
                'errors': {errors}
                """
            )
        )


schema_count = 0


def schemaWrapper(
    model: type[serializers.Serializer]
    # | dict
    | serializers.Serializer
    | serializers.ModelSerializer = None,
):
    """
    Generate Schema Wrapper for Response
    """
    global schema_count
    schema_count = schema_count + 1
    treated_model = None
    if model is not None:
        if inspect.isclass(model):
            treated_model = model()
        else:
            treated_model = model
    class_name = (
        f"SchemaWrapper_{treated_model.__class__.__name__}_{schema_count}"
        if model is not None
        else f"SchemaWrapper_{schema_count}"
    )
    base_classes = (serializers.Serializer,)
    class_attrs = {
        "model": treated_model
        if model is not None
        else serializers.BooleanField(default=True),
        "status_name": serializers.CharField(max_length=100, default="Success"),
        "errors": serializers.ListField(
            child=serializers.CharField(max_length=100),
            allow_null=True,
        ),
    }
    return type(class_name, base_classes, class_attrs)


def enumToDict(model: type[models.Choices]):
    """
    Convert Django Enum to Dict
    """
    choices: list(dict(str | int, str)) = []
    for id, name in model.choices:
        choices.append({"id": id, "name": name})
    return choices


def isBlank(string: str) -> bool:
    return string in (None, "") or not string.strip()


def now() -> datetime.datetime.now:
    return datetime.datetime.now(tz=datetime.timezone.utc)
