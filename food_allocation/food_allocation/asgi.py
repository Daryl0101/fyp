"""
ASGI config for food_allocation project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

# from django.conf.urls import url
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.security.websocket import AllowedHostsOriginValidator
from app_backend.consumers.allocation_consumers import AllocationConsumer
from app_backend.middlewares.wsTokenAuthMiddleware import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_allocation.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            # TokenAuthMiddleware(
            URLRouter([path("ws/allocation", AllocationConsumer.as_asgi())])
            # )
        ),
    }
)
