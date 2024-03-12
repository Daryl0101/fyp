import functools
from typing import Type

from rest_framework import serializers
from rest_framework.response import Response

from .utils import baseResponseSerializerGenerator


def response_handler(responses: Type[serializers.Serializer | dict]):
    """Generalize response handling"""

    def response_handler_inner(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                result = func(request, *args, **kwargs)

            except serializers.ValidationError as e:
                # except Exception as e:
                return Response(
                    baseResponseSerializerGenerator(
                        model=responses,
                        isInstance=True,
                        errors=(
                            # [detail for detail in e.detail]
                            # if type(e.detail) is not serializers.ErrorDetail
                            # else e
                            e
                        ),
                    ).data,
                    status=400,
                )
            return Response(
                baseResponseSerializerGenerator(
                    model=responses,
                    isInstance=True,
                    value=result,
                ).data,
                status=200,
            )

        return wrapper

    return response_handler_inner
