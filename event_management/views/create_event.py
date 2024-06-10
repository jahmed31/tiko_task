from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from event_management.serializers import EventSerializer
from event_management.permissions import IsEventInFuture


class EventCreate(APIView):
    """
    Create an event and return event data as response 
    """
    permission_classes = [permissions.IsAuthenticated, IsEventInFuture]

    @swagger_auto_schema(
        operation_description="Create a new event.",
        request_body=EventSerializer,
        responses={
            201: openapi.Response(description="", schema=EventSerializer),
            400: openapi.Response(description="", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )),
        }
    )
    def post(self, request):
        """
        post function to receive data as post for the event
        :param request: request object (obj)
        :return: Json response (json)
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
