from rest_framework import routers
from app_backend.views.authenticationViews import AuthenticationViews

router = routers.SimpleRouter()
router.register(r"authentication", AuthenticationViews, basename="authentication")
