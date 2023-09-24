from rest_framework import routers
from app_backend.views.authenticationViews import AuthenticationViewset

router = routers.SimpleRouter()
router.register(r"authentication", AuthenticationViewset, basename="authentication")
