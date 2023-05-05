from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from campings.models import CampGround
from campings.serializers import CampGroundSerializer


class CampGroundViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CampGroundSerializer
    queryset = CampGround.objects.all()

    lookup_field = "id"
    lookup_url_kwarg = "campGround_id"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
