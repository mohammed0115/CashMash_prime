# from registerCard.views import RegisterGolenCard,RegisterAgentCard,registerSilverCard,VirtualCard,RegisterList
# from registerCard.views import registerSilverCard
# from registerCard.views import RegisterGolenCard
# from registerCard.views import RegisterAgentCard
# from registerCard.views import VirtualCard
# from registerCard.views import RegisterList
from django.views.decorators.csrf import csrf_exempt
from django.urls import path,include
from IpinGeneration.views import get_public_key,doGenerateIPinRequest,doGenerateCompletionIPinRequest
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
urlpatterns = [
    
    path(
        "IpinGeneration/key/",
        csrf_exempt(get_public_key),
        name="IpinGeneration_key",
    ),
   path(
        "IpinGeneration/generate/",
        csrf_exempt(doGenerateIPinRequest),
        name="doGenerateIPinRequest",
    ),
    path(
        "IpinGeneration/valideIpin/",
        csrf_exempt(doGenerateCompletionIPinRequest),
        name="valideIpin",
    ),
    #
]

