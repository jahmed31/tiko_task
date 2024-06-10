from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from event_management.models import Event
from event_management.serializers import EventSerializer


class AllEventsList(APIView):
    """
    Get all events created by all users
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all events created by all users.",
        responses={
            200: openapi.Response(description="",
                                  schema=EventSerializer(many=True)),
            403: openapi.Response(description="Permission denied"),
        }
    )
    def get(self, request):
        """
        function to get list of all events by users
        :param request: request object (obj)
        :return: json response as list (json)
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
