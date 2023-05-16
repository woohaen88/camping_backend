from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.exceptions import (
    AuthenticationFailed,
    ParseError,
)

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
        get_user_model().objects.create_user(email=email, password=password1)


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
        instance = get_user_model().objects.get(id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
