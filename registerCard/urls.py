# from registerCard.views import RegisterGolenCard,RegisterAgentCard,registerSilverCard,VirtualCard,RegisterList
# from registerCard.views import registerSilverCard
# from registerCard.views import RegisterGolenCard
# from registerCard.views import RegisterAgentCard
# from registerCard.views import VirtualCard
# from registerCard.views import RegisterList
from django.views.decorators.csrf import csrf_exempt
from django.urls import path,include
from registerCard.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path(
        "register/Golden/",
        RegisterGolenCard.as_view(),
     
    ),
    path(
        "register/Agent/",
        csrf_exempt(RegisterStandardCard),
        name="register_Agent",
    ),
    path(
        "register/Silver/",
        csrf_exempt(RegisterStandardCard),
        name="register_Silver",
    ),
   path(
        "register/Virtual/",
        csrf_exempt(RegisterVirtualCard),
        name="register_VirtualCard",
    ),
    path(
        "register/standard/",
        csrf_exempt(RegisterStandardCard),
        name="standard_card",
    ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
