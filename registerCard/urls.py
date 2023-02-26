from django.views.decorators.csrf import csrf_exempt
#from django.conf.urls import url,include
from django.urls import path,include
from .views import (
    RegisterGolenCard,
    RegisterAgentCard,
    registerSilverCard,
    registerSilverCard,
    RegisterList
    
)

urlpatterns = [
    path(
        "register/Golden/",
        csrf_exempt(RegisterGolenCard.as_view()),
        name="register_golden",
    ),
    path(
        "register/Agent/",
        csrf_exempt(RegisterAgentCard.as_view()),
        name="register_Agent",
    ),
    path(
        "register/Silver/",
        csrf_exempt(registerSilverCard.as_view()),
        name="register_Silver",
    ),
   path(
        "register/Virtual/",
        csrf_exempt(registerSilverCard.as_view()),
        name="register_VirtualCard",
    ),
    path(
        "register/List/",
        csrf_exempt(RegisterList.as_view()),
        name="listCard",
    ),
]
