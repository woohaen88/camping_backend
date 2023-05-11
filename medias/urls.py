from django.urls import path

from medias.views import GetImageUrlCloudFlareAPIView

app_name = "medias"
urlpatterns = [
    path(
        "photo/get-url/",
        GetImageUrlCloudFlareAPIView.as_view(),
        name="photo-get-url",
    ),
]
