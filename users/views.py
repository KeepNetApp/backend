from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import GetMeSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_me(request):

    serializer = GetMeSerializer(request.user)
    return Response(serializer.data)
