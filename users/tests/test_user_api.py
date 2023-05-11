from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


LOGIN_URL = reverse("users:log-in")


def create_user(**kwargs):
    defaults = dict(
        email="user@example.com",
        password="test123!@#",
    )
    defaults.update(kwargs)
    return get_user_model().objects.create_user(**defaults)


class UserAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        create_user()

    def test_login_user(self):
        """올바른 자격증명 데이터 => success"""
        payload = dict(email="user@example.com", password="test123!@#")
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status, status.HTTP_200_OK)

    def test_invalid_credentials_login_error(self):
        """유효하지않은 자격증명 데이터 => Bad Request"""
        pass
