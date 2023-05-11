from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
import os

from rest_framework.test import APIClient
from rest_framework import status

# custom
from campings.models import CampGround
from tags.models import Tag
from campings.serializers import CampGroundListSerializer, CampGroundDetailSerializer

CAMPGROUND_URL = reverse("campings:list")


def detail_url(campground_id: str):
    return reverse("campings:detail", args=[campground_id])


CampGround_URL = "http://localhost:8000/api/v1/camping/"
BASE_PAYLOAD = dict(
    check_in="2022-12-21",
    check_out="2023-12-23",
    ratings=3,
    description="",
    address="test address",
    name="sample",
)


def create_campground(owner, **params):
    """Create and return a sample campground"""
    defaults = dict(
        price=3000,
        address="address 입니다.",
        description="description 입니다.",
        pet_friendly=False,
        ev_friendly=True,
        check_in="2023-11-11",
        check_out="2023-11-13",
        ratings=4,
        name="name!!!",
    )

    defaults.update(params)
    campground = CampGround.objects.create(owner=owner, **defaults)
    return campground, defaults


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCampgroundAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CAMPGROUND_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        PAYLOAD = dict(
            price=3000,
            address="address 입니다.",
            description="description 입니다.",
            pet_friendly=False,
            ev_friendly=True,
            check_in="2023-11-11",
            check_out="2023-11-13",
            ratings=4,
            name="name!!!",
        )
        res = self.client.post(CAMPGROUND_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCampgroundAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com",
            password="test123!@#",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_campground(self):
        """Test retrieving a list of campgrounds"""
        create_campground(owner=self.user)
        _, PAYLOAD = create_campground(owner=self.user)

        res = self.client.get(CAMPGROUND_URL)

        campgrounds = CampGround.objects.all()
        serializer = CampGroundListSerializer(campgrounds, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_campground_detail(self):
        """Test get camping detail"""
        campground, _ = create_campground(self.user)
        url = detail_url(campground.id)
        res = self.client.get(url)

        serializer = CampGroundDetailSerializer(campground)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_campground(self):
        """Test creating a campground"""
        PAYLOAD = dict(
            price=3000,
            address="address 입니다.",
            description="description 입니다.",
            pet_friendly=False,
            ev_friendly=True,
            check_in="2023-11-11",
            check_out="2023-11-13",
            ratings=4,
            name="name!!!",
        )
        res = self.client.post(
            CAMPGROUND_URL,
            PAYLOAD,
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        campground = CampGround.objects.get(id=res.data["id"])

        self.assertEqual(
            CampGroundDetailSerializer(campground).data,
            res.data,
        )

        self.assertEqual(campground.owner, self.user)

    def test_create_campground_invalid_date(self):
        """Test creating a campground"""
        PAYLOAD = dict(
            price=3000,
            address="address 입니다.",
            description="description 입니다.",
            pet_friendly=False,
            ev_friendly=True,
            check_in="2023-11-14",
            check_out="2023-11-13",
            ratings=4,
            name="name!!!",
        )
        res = self.client.post(
            CAMPGROUND_URL,
            PAYLOAD,
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update(self):
        """Test full update of campground"""
        campground, payload = create_campground(self.user)

        payload = dict(
            price=5000,
            address="update address 입니다.",
            description="update description 입니다.",
            pet_friendly=True,
            ev_friendly=False,
            check_in="2023-12-11",
            check_out="2023-12-25",
            ratings=5,
            name="update name!!!",
        )

        url = detail_url(campground.id)
        res = self.client.put(
            url,
            payload,
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        campground.refresh_from_db()

        self.assertEqual(
            CampGroundDetailSerializer(campground).data,
            res.data,
        )

        self.assertEqual(campground.owner, self.user)

    def test_partial_update(self):
        """Test partial update of campground"""
        payload = dict(
            name="update name!!!",
        )

        campground, _ = create_campground(self.user)
        url = detail_url(campground.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        campground = CampGround.objects.get(id=res.data["id"])
        self.assertEqual(payload["name"], campground.name)
        self.assertEqual(
            CampGroundDetailSerializer(campground).data,
            res.data,
        )

    def test_update_user_returns_error(self):
        """다른 유저가 업데이트 하면 permission error"""
        new_user = create_user(email="user2@example.com", password="test123!@#")
        campground, _ = create_campground(new_user)

        payload = dict(name="update name")
        url = detail_url(campground.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_camping(self):
        """인증된 유저 삭제 -> 성공"""
        campground, _ = create_campground(self.user)
        url = detail_url(campground.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(CampGround.objects.all()), 0)

    def test_delete_camping_other_user(self):
        """인증된 유저 삭제 -> permission Error"""
        new_user = create_user(
            email="user2@example.com",
            password="test123!@#",
        )
        campground, _ = create_campground(new_user)

        url = detail_url(campground.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(CampGround.objects.all()), 1)

    def test_create_camping_with_new_tags(self):
        """새로운 태그를 이용하여 campground 생성 -> Bad request"""
        payload = dict(
            price=3000,
            address="address 입니다.",
            description="description 입니다.",
            pet_friendly=False,
            ev_friendly=True,
            check_in="2023-11-11",
            check_out="2023-11-13",
            ratings=4,
            name="name!!!",
            tags=[1, 2],
        )
        res = self.client.post(
            CAMPGROUND_URL,
            payload,
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_camping_with_existing_tags(self):
        """존재하는 태그를 이용하여 campground 생성 -> success"""
        Tag.objects.create(name="tag1")
        Tag.objects.create(name="tag2")

        payload = dict(
            price=3000,
            address="address 입니다.",
            description="description 입니다.",
            pet_friendly=False,
            ev_friendly=True,
            check_in="2023-11-11",
            check_out="2023-11-13",
            ratings=4,
            name="name!!!",
            tags=[1, 2],
        )

        res = self.client.post(
            CAMPGROUND_URL,
            payload,
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        campground = CampGround.objects.get(id=res.data["id"])

        self.assertEqual(
            res.data,
            CampGroundDetailSerializer(campground).data,
        )
