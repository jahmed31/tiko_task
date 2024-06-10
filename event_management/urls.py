from django.urls import path
from event_management.views import *

urlpatterns = [
    path('create/', EventCreate.as_view(), name='event-create'),
    path('user/', UserEventsList.as_view(), name='user-events'),
    path('all/', AllEventsList.as_view(), name='all-events'),
    path('update/<int:pk>/', EventUpdate.as_view(), name='event-edit'),
    path('register/<int:pk>/', RegisterForEvent.as_view(), name='event-register'),
    path('unregister/<int:pk>/', UnregisterFromEvent.as_view(), name='event-unregister'),
]
