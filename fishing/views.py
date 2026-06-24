from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fishing.serializers import CatchesSyncSerializer, SessionsSyncSerializer, CatchSyncResponseSerializer, SessionSyncResponseSerializer

from fishing.services import sync_sessions_from_payload, sync_catches_from_payload, get_sync_data


# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sync_pull(request):
    since = request.query_params.get("since", None)
    data = get_sync_data(request.user, since)
    # TODO


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_sessions(request):
    serializer = SessionsSyncSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = sync_sessions_from_payload(request.user, serializer.validated_data)

    response_serializer = SessionSyncResponseSerializer(result)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_catches(request):
    serializer = CatchesSyncSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = sync_catches_from_payload(request.user, serializer.validated_data)

    response_serializer = CatchSyncResponseSerializer(result)
    return Response(response_serializer.data, status=status.HTTP_200_OK)
