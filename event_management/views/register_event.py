from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from event_management.models import Event


class RegisterForEvent(APIView):
    """
    Register user for the event
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Register an user for an event.",
        responses={
            200: openapi.Response(description="", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Registration status')
                }
            )),
            400: openapi.Response(description="", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Cannot register for past events')
                }
            )),
            404: openapi.Response(description="Event not found")
        }
    )
    def post(self, request, pk):
        """
        function to add user in the event
        :param request: request object (obj)
        :param pk: event id (int)
        :return: json response as dict (json)
        """
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if event.start_date < datetime.today().date():
            return Response(
                {'error': 'Cannot register for past events'},
                status=status.HTTP_400_BAD_REQUEST
            )

        event.attendees.add(request.user)
        event.save()
        return Response({'status': 'user registered'}, status=status.HTTP_200_OK)
