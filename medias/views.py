from django.urls import reverse
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response
from medias.serializers import PhotoSerializer
import requests
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser


class GetImageUrlCloudFlareAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        ACCOUNT_ID = settings.CF_ID
        API_TOKEN = settings.CF_TOKEN

        direct_upload_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/images/v2/direct_upload"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        res = requests.post(
            direct_upload_endpoint,
            headers=headers,
        )

        result = res.json().get("result", None)
        if result is None:
            raise ParseError("result값이 None임")

        response_data = {
            "id": result.get("id"),
            "uploadURL": result.get("uploadURL"),
            "success": True,
        }

        if res:
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
