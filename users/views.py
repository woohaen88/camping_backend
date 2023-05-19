from django.conf import settings
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout,
)

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.exceptions import (
    AuthenticationFailed,
    ParseError,
    NotAuthenticated,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticated
from users.serializers import SignUpSerializer, LoginSerializer, MeSerializer


class SignUPViewSet(ModelViewSet):
    serializer_class = SignUpSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer, **kwargs):
        email = self.request.data.get("email")
        password1 = self.request.data.get("password1")
        password2 = self.request.data.get("password2")
        user = get_user_model().objects.create_user(email=email, password=password1)
        login(self.request, user)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")

            user = authenticate(
                request,
                username=email,
                password=password,
            )

            if user:
                login(request, user)
                return Response(
                    {"message": "login success"},
                    status=status.HTTP_200_OK,
                )
            raise AuthenticationFailed("Invalid Credentials")

        raise ParseError("Bad request!!")


class MeView(RetrieveAPIView):
    serializer_class = MeSerializer

    def retrieve(self, request, *args, **kwargs):
        if request.user.id is not None:
            instance = get_user_model().objects.get(id=request.user.id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        raise PermissionDenied("Login 되지 않음")


class LogOutView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user is not None:
            logout(request)
            return Response({"message": "logout success"}, status=status.HTTP_200_OK)
        raise PermissionDenied("Logout 되지 않음")


class KakaoView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        code = request.data.get("code", None)
        if code is None:
            raise ParseError
        url: str = "https://kauth.kakao.com/oauth/token"
        res = requests.post(
            url,
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_REST_API_KEY,
                "code": code,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        res = res.json()

        access_token = res.get("access_token", None)
        if access_token is None:
            raise ParseError

        res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        res = res.json()

        kakao_account = res.get("kakao_account")
        # user 정보
        email = kakao_account.get("email")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        avatar = profile.get("thumbnail_image_url")

        print("email: ", email)
        print("nickname: ", nickname)
        print("avatar: ", avatar)
        print("profile: ", profile)

        # 유저가 존재하는지 확인
        #      유저가 존재하면 로그인으로 진행
        # 유저가 존재하지 않으면 계정생성 후 로그인

        try:
            # 유저가 존재하면
            user = get_user_model().objects.get(
                email=email,
                create_via=get_user_model().CreateViaChoice.KAKAO,
            )

        except:
            # 유저가 없으면
            user = get_user_model().objects.create(
                email=email,
                username=nickname,
                avatar=avatar,
                create_via=get_user_model().CreateViaChoice.KAKAO,
            )
            user.set_unusable_password()
            user.save()

        login(request, user)
        return Response(
            {"deatil": "login success"},
            status=status.HTTP_200_OK,
        )
