from rest_framework.views import APIView

from api.classes import Manager_Config
from api.serializers import Serializer_Config
from mturk_db.permissions import AllowOptionsAuthentication, IsInstance
from rest_framework.response import Response

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Config(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    def get(self, request):
        config = Manager_Config.get_config()

        serializer = Serializer_Config(config)

        return Response(serializer.data)