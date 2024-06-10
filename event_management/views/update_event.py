from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from event_management.models import Event
from event_management.serializers import EventSerializer
from event_management.permissions import IsOwnerOrReadOnly, IsEventInFuture


class EventUpdate(APIView):
    """
    Update an event and return event data as response
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly, IsEventInFuture]

    @swagger_auto_schema(
        operation_description="Update an event entirely.",
        request_body=EventSerializer,
        responses={
            200: openapi.Response(description="", schema=EventSerializer),
            400: openapi.Response(description="", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )),
            404: openapi.Response(description="Event not found")
        }
    )
    def put(self, request, pk):
        """
        function to update already existed event record
        :param request: request object (obj)
        :param pk: id of event (int)
        :return: json response as dictionary (json)
        """
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, event)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an event.",
        request_body=EventSerializer,
        responses={
            200: openapi.Response(description="", schema=EventSerializer),
            400: openapi.Response(description="Attendee not available", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )),
            404: openapi.Response(description="")
        }
    )
    def patch(self, request, pk):
        """
        function to patch the already existed event record
        :param request: request object (obj)
        :param pk: id of event (int)
        :return: json response as dictionary (json)
        """
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, event)

        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
