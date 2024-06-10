from django.urls import path
from user_profile.views import UserRegistration

urlpatterns=[
    path('register/', UserRegistration.as_view(), name='user-register'),
]
