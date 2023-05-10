from django.test import TestCase
from django.contrib.auth import get_user_model
import os

from rest_framework.test import APIClient
from rest_framework import status

# custom
from campings.models import CampGround

CampGround_URL = "http://localhost:8000/api/v1/camping/"
BASE_PAYLOAD = dict(
    check_in="2022-12-21",
    check_out="2023-12-23",
    ratings=3,
    description="",
    address="test address",
    name="sample",
)


def detail_url(campground_id) -> str:
    url = f"{CampGround_URL}{campground_id}/"
    return url


def create_user(**kwargs):
    email = kwargs.pop("email", None)
    password = kwargs.pop("password", None)

    if email is not None and password is not None:
        user = get_user_model().objects.create_user(email, password)
        return user
    raise ValueError("email과 password가 없습니다.")


def create_camping(owner, **kwargs) -> CampGround:
    payload = BASE_PAYLOAD
    for k, v in kwargs.items():
        payload[k] = v

    campground = CampGround.objects.create(owner=owner, **payload)
    return campground


class PrivateModelTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user(email="user@example.com", password="test123!@#")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_campground_model(self):
        """모델을 만들었을 때 name객체가 출력되어야함"""
        campGround = CampGround.objects.create(
            owner=self.user,
            check_in="2022-12-21",
            check_out="2023-12-23",
            ratings=3,
            description="",
            address="test address",
            name="sample",
        )

        self.assertEqual(str(campGround), campGround.name)


class PublicModelTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.post(CampGround_URL, BASE_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_url_success(self):
        res = self.client.get(CampGround_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), len(CampGround.objects.all()))


class PrivateCampGroundModelTest(TestCase):
    def setUp(self) -> None:
        self.BASE_USER_EMAIL = "user@example.com"
        self.client = APIClient()
        self.user = create_user(email=self.BASE_USER_EMAIL, password="test123!@#")
        self.client.force_login(self.user)

    def test_post_CampGround(self):
        payload = dict(
            check_in="2022-12-21",
            check_out="2023-12-23",
            ratings=3,
            description="",
            address="test address",
            name="sample",
        )
        res = self.client.post(CampGround_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        campGround = CampGround.objects.get(owner=self.user)

        for key, value in payload.items():
            if key in ["check_in", "check_out"]:  # 날짜
                self.assertEqual(getattr(campGround, key).strftime("%Y-%m-%d"), value)
            else:
                self.assertEqual(getattr(campGround, key), value)

    def test_get_CampGround_detail(self):
        """detail url로 접속했을 때 결과"""
        campground = create_camping(self.user)
        url = detail_url(campground.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res_owner = res.data.get("owner")

        self.assertEqual(self.BASE_USER_EMAIL, res_owner["email"])
        for key, value in BASE_PAYLOAD.items():
            self.assertEqual(getattr(campground, key), value)

    def test_full_update_campground_detail(self):
        """detail URL 전체수정"""
        campground = create_camping(self.user)

        PAYLOAD = dict(
            check_in="2022-12-24",
            check_out="2023-12-30",
            ratings=5,
            description="수정",
            address="test update address",
            name="sample update",
        )

        url = detail_url(campground.id)

        res = self.client.put(url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        campground.refresh_from_db()
        campground = CampGround.objects.get(owner=self.user)
        for key, value in PAYLOAD.items():
            if key in ["check_in", "check_out"]:  # 날짜
                self.assertEqual(getattr(campground, key).strftime("%Y-%m-%d"), value)
            else:
                self.assertEqual(getattr(campground, key), value)
        self.assertEqual(self.user, campground.owner)

    def test_full_partial_update_campground_detail(self):
        """detail URL 부분수정"""
        campground = create_camping(self.user)

        PAYLOAD = dict(
            name="partial sample update",
        )

        url = detail_url(campground.id)

        res = self.client.patch(url, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        campground.refresh_from_db()
        campground = CampGround.objects.get(owner=self.user)
        for key, value in BASE_PAYLOAD.items():
            if key in ["check_in", "check_out"]:  # 날짜
                self.assertEqual(getattr(campground, key).strftime("%Y-%m-%d"), value)
            elif key == "name":
                self.assertEqual(getattr(campground, key), PAYLOAD["name"])
            else:
                self.assertEqual(getattr(campground, key), value)
        self.assertEqual(self.user, campground.owner)

    def test_full_delete_campground_detail(self):
        """detail 삭제"""
        campground = create_camping(self.user)

        url = detail_url(campground.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_date_validate_campground_detail(self):
        """체크인이 체크아웃보다 느릴수 없음"""
        PAYLOAD = BASE_PAYLOAD.copy()

        PAYLOAD["check_in"] = "2023-12-21"
        PAYLOAD["check_out"] = "2023-11-21"

        res = self.client.post(CampGround_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        PAYLOAD["check_in"] = "2023-12-21"
        PAYLOAD["check_out"] = "2023-12-21"

        res = self.client.post(CampGround_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
