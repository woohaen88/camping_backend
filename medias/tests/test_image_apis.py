from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from PIL import Image
import tempfile

GET_UPLOAD_URL = reverse("medias:photo-get-url")
UPLOAD_URL = reverse("medias:photo-uploads")


def create_user(**kwargs):
    defaults = dict(
        email="user@example.com",
        password="test123!@#",
    )

    defaults.update(kwargs)

    user = get_user_model().objects.create_user(**defaults)
    if user:
        return user
    raise ValueError("user 객체가 만들어지지 않았음")


class PublicImageTestAPIs(TestCase):
    pass


class PrivateImageTestAPIs(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_upload_url_success(self):
        res = self.client.post(GET_UPLOAD_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data.get("success"))

    def test_upload_multiple_file(self):
        upload_url = reverse("medias:photo-uploads")

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            image_list = []
            for i in range(3):
                img = Image.new("RGB", (10, 10))
                img.save(image_file, format="JPEG")
                image_file.seek(0)
                image_payload = {
                    "file": image_file,
                    "description": "",
                }
                image_list.append(image_payload)
            payload = {"photos": image_list}

            res = self.client.post(upload_url, payload, format="multipart")
            # print("res.data: ", res.data)
