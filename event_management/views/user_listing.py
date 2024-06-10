from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from event_management.models import Event
from event_management.serializers import EventSerializer


class UserEventsList(APIView):
    """
    Get user specific events
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of events created by user.",
        responses={
            200: openapi.Response(description="",
                                  schema=EventSerializer(many=True)),
            403: openapi.Response(description="Permission denied"),
        }
    )
    def get(self, request):
        """
        function to get user specific events list
        :param request: request object (obj)
        :return: json response as list (json)
        """
        events = Event.objects.filter(owner=request.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
