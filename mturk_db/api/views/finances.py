from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.classes.finances import ManagerFinances
from api.helpers import add_database_object_project
from api.serializers import Serializer_Finances
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Finances(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        data = ManagerFinances.get(
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
            request=request
        )

        serializer = Serializer_Finances(
            data,
        )

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def get_balance(request, slug_project, database_object_project, use_sandbox, format=None):
    balance = ManagerFinances.get_balance(use_sandbox=use_sandbox)
    return Response(balance)
