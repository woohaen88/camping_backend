from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from users.serializers import MeSerializer

LOGIN_URL = reverse("users:log-in")
ME_URL = reverse("users:me")
LOGOUT_URL = reverse("users:log-out")


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

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("message"), "login success")

    def test_invalid_credentials_login_error(self):
        """유효하지않은 자격증명 데이터 => Bad Request"""
        payload = dict(email="user@example.com", password="test123!@#$")
        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_me(self):
        """나의 정보 확인"""

        user = create_user(email="user1@example.com")
        self.client.force_authenticate(user)
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        userObj = get_user_model().objects.get(id=res.data["id"])
        serializer = MeSerializer(userObj)

        self.assertEqual(serializer.data, res.data)

    def test_logout(self):
        user = create_user(email="user1@example.com")
        self.client.force_authenticate(user)

        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
