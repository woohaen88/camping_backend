from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from campings.models import CampGround

CampGroundURL = "http://localhost:8000/api/v1/camping/"

BASE_PAYLOAD = dict(
    check_in="2022-12-21",
    check_out="2023-12-23",
    ratings=3,
    description="",
    address="test address",
    name="sample",
    tags=[1, 2],
)


def create_user(**kwargs):
    email = kwargs.pop("email", None)
    password = kwargs.pop("password", "test123!@#")

    if email is None or password is None:
        raise ValueError("email이나 password는 빈값이 아니여야함")

    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        **kwargs,
    )
    return user


def create_campground(owner, **kwargs) -> CampGround:
    PAYLOAD = BASE_PAYLOAD.copy()
    if kwargs:
        for k, v in kwargs.items():
            PAYLOAD[k] = v

    campground = CampGround.objects.create(owner=owner, **PAYLOAD)
    return campground


class PublicCreateOrGetCamping(TestCase):
    def setUp(self) -> None:
        self.user = create_user(email="test@example.com")
        self.client = APIClient()

    def test_create_camping_with_tag_permission_error(self):
        PAYLOAD = BASE_PAYLOAD.copy()

        res = self.client.post(CampGroundURL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_camping_with_tag_result_non_error(self):
        res = self.client.get(CampGroundURL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateCRUDCamping(TestCase):
    def setUp(self) -> None:
        self.user = create_user(email="test@example.com")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_camping_with_tag_success(self):
        """조회 하면 태그도 같이 나와야함"""
        # create_campground(self.user)
        # campground = CampGround.objects.get(owner=self.user)

        # res = self.client.get(CampGroundURL)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)

        # PAYLOAD = BASE_PAYLOAD.copy()
        # for k, v in PAYLOAD.items():
        #     self.assertEqual(getattr(campground, k), v)
        pass

    def test_create_camping_with_tag_success(self):
        """태그와 같이 요청시 201"""
        PAYLOAD = BASE_PAYLOAD.copy()
        res = self.client.post(CampGroundURL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_OK)

        campground = CampGround.objects.get(owner=self.user)

        for k, v in PAYLOAD.items():
            self.assertEqual(getattr(campground, k), v)

    def test_update_camping_with_tag_success(self):
        """업데이트 하면 태그도 같이 나와야함"""
        pass

    def test_update_camping_with_tag_success(self):
        """
        업데이트 하면 태그도 같이 나와야함
        업데이트 할 때 체크인 날짜 >= 체크아웃 날짜 --> 400 error
        """
        pass

    def test_partial_update_camping_with_tag_success(self):
        """부분업데이트 태그도 같이 나와야함"""
        pass

    def test_delete_camping_with_tag_success(self):
        """캠핑 컨텐츠 삭제"""
        pass
