from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView

from users.serializers import SignUpSerializer, LoginSerializer


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
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        request_data = self.request.data
        serializer.save(
            email=request_data["email"],
            password=request_data["password"],
            username=request_data["username"],
        )
