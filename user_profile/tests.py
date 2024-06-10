import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def valid_user_data(self):
        return {
            'password': 'testpassword',
            'email': 'testuser@example.com'
        }

    @pytest.fixture
    def invalid_user_data(self):
        return {
            'password': 'testpassword',
            'email': ''
        }

    def test_register_user_success(self, api_client, valid_user_data):
        url = reverse('user-register')
        response = api_client.post(url, valid_user_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data

    def test_register_user_fail(self, api_client, invalid_user_data):
        url = reverse('user-register')
        response = api_client.post(url, invalid_user_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_user_duplicate(self, api_client, valid_user_data):
        User.objects.create_user(**valid_user_data)
        url = reverse('user-register')
        response = api_client.post(url, valid_user_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
