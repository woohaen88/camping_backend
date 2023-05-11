from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from campings.models import CampGround
from campings.serializers import CampGroundDetailSerializer, CampGroundListSerializer


class CampGroundViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CampGroundDetailSerializer
    queryset = CampGround.objects.all()

    lookup_field = "id"
    lookup_url_kwarg = "campGround_id"

    def get_serializer_class(self):
        if self.action == "list":
            return CampGroundListSerializer
        return super().get_serializer_class()

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

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            tags=self.request.data.get("tags"),
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            raise NotAuthenticated

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            raise NotAuthenticated

        return super().destroy(request, *args, **kwargs)
