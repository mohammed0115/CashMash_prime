from rest_framework.views import APIView
from rest_framework_jwt import views as jwt_views
from rest_framework.response import Response
from .utils import generate_jwt_token_payload, encode_jwt_token_payload
from rest_framework.exceptions import APIException
# Create your views here.
from APIKEY.models import BlockedToken

class ObtainJSONWebTokenAPIView(jwt_views.ObtainJSONWebToken):
    """
    This view allows us to use a different jwt_response_payload_handler in the view.
    Usually jwt_response_payload_handler is configured in the django settings file for global use.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.object.get('user') or request.user
                token = serializer.object.get('token')
                d,j=BlockedToken.objects.update_or_create(token=token,User=user)
                d.save()
                response_data = self.get_response_payload(token, user, request)
                response = Response(response_data)
                return response
        except APIException as e:
            status_code = 400
            return Response({
                             "responseStatus":"Failed","responseCode":status_code,"responseMessage":str(e)},
                    status=200
                    )
        
    def get_response_payload(self, token, user=None, request=None):
        return {'token': token}


class BaseRefreshUserTokenView(APIView):
    username_field = None

    def post(self, request, *args, **kwargs):
        try:
            payload = generate_jwt_token_payload(request.user, self.username_field)
            token = encode_jwt_token_payload(payload)
            response_data = {'token': token,"responseStatus":"Successful","responseCode":0,"responseMessage":"Approval" }
            response = Response(response_data)
            return response
        except APIException as e:
            status_code = 400
            return Response({
                             "responseStatus":"Failed","responseCode":status_code,"responseMessage":str(e)},
                    status=200
                    )
        
