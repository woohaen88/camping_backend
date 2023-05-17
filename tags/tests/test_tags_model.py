from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.shortcuts import reverse
from tags.models import Tag

from tags.serializers import TagSerializer

TAG_URL = reverse("tags:list_or_create")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PrivateTestTagModel(TestCase):
    def setUp(self) -> None:
        user = create_user(
            email="user@example.com",
            password="test123!@#",
        )
        self.client = APIClient()
        self.client.force_authenticate(user)

        Tag.objects.create(name="tag1")
        Tag.objects.create(name="tag2")
        Tag.objects.create(name="tag3")

    def test_createTag_error(self):
        """
        모델 생성시 slug도 존재해야함
        str -> name
        """

        PAYLOAD = dict(
            name="sample1",
        )
        tag = Tag.objects.create(**PAYLOAD)
        self.assertEqual(str(tag), PAYLOAD["name"])

        self.assertTrue(tag.slug)
        self.assertEqual(tag.name, PAYLOAD["name"])

    def test_get_all_tags(self):
        """모든 태그 조회"""
        tags = Tag.objects.all()

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.data, serializer.data)
