import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


@pytest.mark.django_db
class TestEventCreate:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user_data(self):
        return {'email': 'testuser@test.com', 'password': 'testpassword'}

    @pytest.fixture
    def test_user(self, user_data):
        return User.objects.create_user(
            email=user_data['email'], password=user_data['password']
        )

    @pytest.fixture
    def auth_token(self, api_client, test_user, user_data):
        url = reverse('token_obtain_pair')
        response = api_client.post(url, data=user_data, follow=True)
        token = response.data['access']
        return token

    @pytest.fixture
    def auth_headers(self, api_client, auth_token):
        return api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_token)

    @pytest.fixture
    def valid_event_data(self):
        return {
            'name': 'Test Event',
            'description': 'Test Description',
            'start_date': '15-06-2025',
            'end_date': '16-06-2025',
            'owner': 1
        }

    @pytest.fixture
    def invalid_event_data(self):
        return {
            'name': '',
            'description': 'Test Description',
            'start_date': '15-06-2025',
            'end_date': '16-06-2025',
            'owner': 1
        }

    def test_create_event_success(self, api_client, auth_headers, valid_event_data):
        url = reverse('event-create')
        response = api_client.post(url, valid_event_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data

    def test_create_event_fail(self, api_client, auth_headers, invalid_event_data):
        url = reverse('event-create')
        response = api_client.post(url, invalid_event_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
