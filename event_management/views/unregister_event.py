from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from event_management.models import Event


class UnregisterFromEvent(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Unregister an authenticated user from an event.",
        responses={
            200: openapi.Response(description="", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Unregistration status')
                }
            )),
            400: openapi.Response(description="", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='')
                }
            )),
            404: openapi.Response(description="")
        }
    )
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user not in event.attendees.all():
            return Response(
                {'error': 'User not registered for this event'},
                status=status.HTTP_400_BAD_REQUEST
            )

        event.attendees.remove(request.user)
        event.save()
        return Response({'status': 'unregistered'}, status=status.HTTP_200_OK)
