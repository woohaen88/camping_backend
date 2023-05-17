from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
