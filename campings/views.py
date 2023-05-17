from django.utils.datastructures import MultiValueDict
from rest_framework.parsers import (
    MultiPartParser,
    JSONParser,
    FormParser,
    FileUploadParser,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from campings.models import CampGround
from campings.serializers import CampGroundDetailSerializer, CampGroundListSerializer
from medias.models import Photo
from medias.serializers import PhotoSerializer
from ast import literal_eval


class CampGroundViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CampGroundDetailSerializer
    queryset = CampGround.objects.all().order_by("-updated_at")
    parser_classes = [
        MultiPartParser,
        JSONParser,
        FormParser,
        FileUploadParser,
    ]

    lookup_field = "id"
    lookup_url_kwarg = "campGround_id"

    def get_serializer_class(self):
        if self.action == "list":
            return CampGroundListSerializer
        return super().get_serializer_class()

    def request_files_save_photo(
        self,
        request,
        campground: CampGround,
        files: MultiValueDict,
    ):
        files_iterator = files.lists()
        files_dict = next(files_iterator)

        files_dict_key, files_dict_value = files_dict

        for file in files_dict_value:
            photo = Photo.objects.create(
                file=file,
                owner=request.user,
                campgrounds=campground,
            )
            photo.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        campground = self.perform_create(serializer)

        # Image

        if request.FILES:
            self.request_files_save_photo(request, campground, request.FILES)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        tags = self.request.data.get("tags", None)
        if tags is None:
            tags = self.request.data.getlist("tags[]")
            if len(tags) == 0:
                tags = None

        return serializer.save(
            owner=self.request.user,
            tags=tags,
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            raise NotAuthenticated

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(files=request.FILES)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

        ###

        # return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user:
            raise NotAuthenticated

        return super().destroy(request, *args, **kwargs)
